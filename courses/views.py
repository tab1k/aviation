from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.timezone import localtime, now
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView

from comments.forms import CommentForm
from comments.models import Comment
from .forms import CourseForm, CourseTypeForm, ModuleForm, LessonForm
from .models import Course, Module, CourseType, Lesson
from django.views import View
from users.models import User
from courses.models import Lesson
from tests.models import TestResult
from essays.models import EssaySubmission
import matplotlib.pyplot as plt
from django.db.models import Count
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from urllib.request import urlopen
from users.models import User


class CoursesByType(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, type_id):
        # Получаем тип курса по type_id или возвращаем 404, если не найден
        course_type = get_object_or_404(CourseType, id=type_id)

        # Получаем все курсы, относящиеся к данному типу курса
        courses = Course.objects.filter(course_type=course_type)

        # Определяем шаблон в зависимости от роли пользователя
        user_group = request.user.groups.first()
        role_templates = {
            'Студенты': 'users/student/courses_by_type.html',
            'Кураторы': 'users/curator/courses_by_type.html',
            'Администраторы': 'users/admin/courses_by_type.html',
        }
        template_name = role_templates.get(user_group.name) if user_group else None

        # Если пользователь не аутентифицирован или не принадлежит ни к одной из групп,
        # перенаправляем его на страницу входа
        if not template_name:
            return redirect('users:login')

        return render(request, template_name, {'course_type': course_type, 'courses': courses})


class Courses(ListView):
    model = Course
    context_object_name = 'courses'
    ordering = ['-created_at']

    def get_template_names(self):
        if self.request.user.groups.filter(name='Администраторы').exists():
            return ['users/admin/coursesAfterSignUpAdmin.html']
        elif self.request.user.groups.filter(name='Кураторы').exists():
            return ['users/curator/coursesAfterSignUpCurator.html']
        return ['users/student/coursesAfterSignUp.html']

    def get_queryset(self):
        if self.request.user.groups.filter(name='Администраторы').exists() or self.request.user.groups.filter(
                name='Кураторы').exists():
            return super().get_queryset()
        return Course.objects.filter(students=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = localtime(now())
        context['student_comments'], context['curator_comments'] = self.get_comments()
        return context

    def get_comments(self):
        all_comments = Comment.objects.filter(Q(user=self.request.user) | Q(curator=self.request.user))
        student_comments = all_comments.filter(is_student_comment=True)
        curator_comments = all_comments.filter(is_student_comment=False)
        return student_comments, curator_comments


class Modules(View):
    def get(self, request, pk):
        # Получаем модули для курса с заданным pk
        modules = Module.objects.filter(course__pk=pk)

        # Определяем шаблон в зависимости от роли пользователя
        user_group = request.user.groups.first()
        role_templates = {
            'Администраторы': 'users/admin/module.html',
            'Кураторы': 'users/curator/moduleAdmin.html',
            # Если пользователь не принадлежит ни к одной из групп, используем шаблон для студентов
            'default': 'users/student/module.html',
        }
        template_name = role_templates.get(user_group.name, role_templates['default'])

        # Фильтруем модули в зависимости от роли пользователя
        if user_group:
            if user_group.name == 'Кураторы':
                modules = modules.filter(course__curators=request.user)
            elif user_group.name != 'Администраторы':
                modules = modules.filter(course__students=request.user)

        # Рендерим страницу с переданными в шаблон данными
        return render(request, template_name, {'modules': modules})



# Представление для отображения уроков в модуле
class LessonsByModule(View):

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        lessons = module.lesson_set.all()  # Получаем все уроки модуля

        if request.user.role == 'student':
            return render(request, 'users/student/lessonsStudent.html', {'module': module, 'lessons': lessons})
        elif request.user.role == 'curator':
            return render(request, 'users/curator/lessonsCurator.html', {'module': module, 'lessons': lessons})
        elif request.user.role == 'admin':
            return render(request, 'users/admin/lessonsAdmin.html', {'module': module, 'lessons': lessons})
        else:
            return render(request, 'users/404.html')


class LessonView(View):
    student_template = 'users/student/video.html'
    curator_template = 'users/curator/videoAdmin.html'
    admin_template = 'users/admin/videoAdmin.html'


    def get_next_lesson(self, current_lesson):
        module = current_lesson.module
        next_lesson = Lesson.objects.filter(module=module, id__gt=current_lesson.id).order_by('id').first()
        return next_lesson

    def get_previous_lesson(self, current_lesson):
        module = current_lesson.module
        previous_lesson = Lesson.objects.filter(module=module, id__lt=current_lesson.id).order_by('-id').first()
        return previous_lesson

    def get_comments(self, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        comments = Comment.objects.filter(lesson=lesson)
        comment_list = [{"user": comment.user, "text": comment.text} for comment in comments]
        return JsonResponse({"comments": comment_list})

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        module = lesson.module
        lessons = Lesson.objects.filter(module=module)
        comment_form = CommentForm()
        student_comments = Comment.objects.filter(lesson=lesson, is_student_comment=True)
        student = request.user
        course_type = CourseType.objects.filter(courses__students=student).distinct()
        courses = Course.objects.filter(students=student)


        if request.user.role == 'student':
            next_lesson = self.get_next_lesson(lesson)
            previous_lesson = self.get_previous_lesson(lesson)
            curator_comments = Comment.objects.filter(lesson=lesson, is_student_comment=False, user=student)
            return render(request, self.student_template,
                          {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form,
                           'student_comments': student_comments, 'next_lesson': next_lesson,
                           'previous_lesson': previous_lesson,
                           'courses': courses,
                           'course_type': course_type,
                           'student': student,
                           'curator_comments': curator_comments,
                           'lesson_id': lesson_id  # Передаем идентификатор урока в контекст
                           })
        elif request.user.role == 'curator':
            return render(request, self.curator_template,
                          {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        elif request.user.role == 'admin':
            return render(request, self.admin_template,
                          {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        else:
            return redirect(reverse('users:login'))

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        module = lesson.module
        lessons = Lesson.objects.filter(module=module)
        comment_form = CommentForm(request.POST)  # Инициализируем форму данными из POST-запроса

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.lesson = lesson
            comment.is_student_comment = True
            comment.save()

            # Возвращаем обновленный список комментариев в JSON-ответе
            comments = Comment.objects.filter(lesson=lesson, is_student_comment=True)
            comments_data = [{'user': comment.user.username, 'text': comment.text} for comment in comments]
            return JsonResponse({'success': True, 'comments': comments_data})

        if request.user.role == 'student':
            return render(request, self.student_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        elif request.user.role == 'curator':
            return render(request, self.curator_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        elif request.user.role == 'admin':
            return render(request, self.admin_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        else:
            # Перенаправление на страницу входа
            return redirect(reverse('users:login'))


# Представления для CourseType
class CourseTypeCreateView(CreateView):
    model = CourseType
    form_class = CourseTypeForm
    template_name = 'users/admin/create/course_type_form.html'
    success_url = reverse_lazy('users:admin:courses:courses')


# Представления для Course
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm  # Используем нашу кастомную форму
    template_name = 'users/admin/create/course_form.html'
    success_url = reverse_lazy('users:admin:courses:courses')


# Представления для Module

class ModuleCreateView(CreateView):
    model = Module
    form_class = ModuleForm  # Используем нашу кастомную форму
    template_name = 'users/admin/create/module_form.html'

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs.get('course_id')
        if course_id:
            initial['course'] = course_id
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('course_id'):
            kwargs['initial']['course'] = self.kwargs['course_id']
            kwargs['empty_label'] = None
        return kwargs

    def get_success_url(self):
        return reverse_lazy('users:admin:courses:modules', kwargs={'pk': self.object.course.pk})



# Представления для Lesson
class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'users/admin/create/lesson_form.html'
    success_url = reverse_lazy('users:admin:courses:courses')


class AnswersView(View):
    template_curator = 'users/curator/answers.html'
    template_admin = 'users/admin/answers.html'
    template_error = 'users/404.html'

    def get(self, request):
        student_comments = Comment.objects.filter(is_student_comment=True)

        # Получаем список всех курсов
        all_courses = Course.objects.all()

        # Получаем выбранный курс из параметра запроса
        course_filter = request.GET.get('course_filter')
        module_filter = request.GET.get('module_filter')
        lesson_filter = request.GET.get('lesson_filter')
        student_filter = request.GET.get('student_filter')

        selected_course = None
        selected_module = None
        selected_lesson = None
        selected_student = None  # Добавляем переменную для выбранного студента

        # Фильтруем комментарии по выбранным параметрам
        if course_filter:
            selected_course = Course.objects.filter(id=course_filter).first()
            student_comments = student_comments.filter(lesson__module__course=selected_course)

            if module_filter:
                selected_module = Module.objects.filter(id=module_filter).first()
                student_comments = student_comments.filter(lesson__module=selected_module)

                if lesson_filter:
                    selected_lesson = Lesson.objects.filter(id=lesson_filter).first()
                    student_comments = student_comments.filter(lesson_id=lesson_filter)

            if student_filter:  # Фильтр по студенту
                selected_student = User.objects.filter(id=student_filter).first()
                student_comments = student_comments.filter(user=selected_student)


        if request.user.role == 'curator':
            template_name = self.template_curator
        elif request.user.role == 'admin':
            template_name = self.template_admin
        else:
            template_name = self.template_error

        return render(request, template_name, {
            'comments': student_comments,
            'all_courses': all_courses,
            'selected_course': selected_course,
            'selected_module': selected_module,
            'selected_student': selected_student,
            'is_student_comment': True
        })

    def post(self, request):
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.filter(id=comment_id).first()
            if comment and comment.is_student_comment:
                comment.delete()
        elif 'curator_response' in request.POST:
            comment_id = request.POST.get('comment_id')
            curator_response = request.POST.get('curator_response')
            comment = Comment.objects.filter(id=comment_id, is_student_comment=True).first()
            if comment:
                comment.curator_response = curator_response
                comment.curator = request.user
                comment.is_student_comment = False
                comment.save()

        # Перенаправление в зависимости от роли пользователя
        if request.user.role == 'curator':
            return redirect('users:curator:courses:answers_view')
        elif request.user.role == 'admin':
            return redirect('users:admin:courses:answers_view')
        else:
            # Пользователь не имеет определенной роли, обработайте этот случай по своему усмотрению
            return render(request, 'users/404.html')




class StudentProgressView(View):
    template_name_curator = 'users/curator/student_progress.html'
    template_name_admin = 'users/admin/student_progress.html'

    def get(self, request, student_id):
        if request.user.role not in ['curator', 'admin']:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")

        student = User.objects.get(pk=student_id)
        courses = student.courses.all()

        progress = []
        total_test_scores = 0
        total_essays_submitted = 0
        lessons_titles = []
        test_scores = []
        essays_submitted = []
        total_test_lessons = 0
        total_lessons = 0

        for course in courses:
            modules = course.modules.all()
            for module in modules:
                lessons = module.lesson_set.all()
                for lesson in lessons:
                    test_result = TestResult.objects.filter(student=student, lesson=lesson).first()
                    essay_submission = EssaySubmission.objects.filter(student=student, lesson=lesson).first()

                    if test_result:
                        total_test_scores += test_result.score
                        test_scores.append(test_result.score)
                        total_test_lessons += 1

                    if essay_submission:
                        total_essays_submitted += 1
                        essays_submitted.append(1)
                    else:
                        essays_submitted.append(0)  # Добавляем значение 0 для урока без сданного эссе

                    progress.append({
                        'course': course,
                        'module': module,
                        'lesson': lesson,
                        'test_result': test_result,
                        'essay_submission': essay_submission,
                    })

                    lessons_titles.append(lesson.title)
                    total_lessons += 1

        lesson_count_with_tests = total_test_lessons
        average_test_score = total_test_scores / lesson_count_with_tests if lesson_count_with_tests > 0 else 0

        context = {
            'student': student,
            'progress': progress,
            'average_test_score': average_test_score,
            'total_essays_submitted': total_essays_submitted,
            'lessons_titles': lessons_titles,
            'test_scores': test_scores,
            'essays_submitted': essays_submitted,
        }

        if request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name_admin, context)

# Ваш файл views.py



class PassedStudentsView(View):
    template_name = 'users/admin/passed_students.html'
    template_name_curator = 'users/curator/passed_students.html'


    def get(self, request):
        if request.user.role not in ['curator', 'admin']:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")


        search_query = request.GET.get('q', '')

        passed_students = []
        students = User.objects.filter(role='student')

        for student in students:
            courses = Course.objects.filter(students=student)

            # Check if the student passed all lessons with tests and essays in each course
            for course in courses:
                modules = course.modules.all()
                lessons_passed = 0

                # Check if the student passed all lessons with tests and essays in each module
                for module in modules:
                    lessons_with_tests_and_essays = Lesson.objects.filter(module=module)

                    total_lessons_in_module = lessons_with_tests_and_essays.count()

                    # Check if the student passed all lessons in the module
                    passed_all_lessons_in_module = (
                        lessons_with_tests_and_essays
                        .annotate(test_passed=Count('testresult', filter=Q(testresult__student=student, testresult__score__gte=50)))
                        .annotate(essay_passed=Count('essaysubmission', filter=Q(essaysubmission__student=student)))
                        .filter(test_passed__gte=1, essay_passed__gte=1)
                        .count() == total_lessons_in_module
                    )

                    if passed_all_lessons_in_module:
                        lessons_passed += total_lessons_in_module
                    else:
                        break

                # Check if the student passed all lessons in all modules of the course
                if lessons_passed == Course.objects.get(pk=course.pk).modules.count():
                    passed_students.append(student)
                    break

        # Apply search query if provided
        search_query = request.GET.get('q', None)

        if search_query:
            filtered_students = User.objects.filter(
                Q(role='student'),
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

            passed_students = [student for student in filtered_students if student in passed_students]
        else:
            passed_students = User.objects.filter(id__in=[student.id for student in passed_students])

        selected_course_id = request.GET.get('course_filter')

        if selected_course_id:
            selected_course = Course.objects.get(pk=selected_course_id)
            passed_students = [student for student in passed_students if selected_course in student.courses.all()]

        all_courses = Course.objects.all()

        context = {
            'passed_students': passed_students,
            'search_query': search_query,
            'all_courses': all_courses,
            'selected_course_id': selected_course_id,
        }

        if request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name, context)


import tempfile
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
import calendar
import locale


class CertificateView(View):
    def get(self, request, student_id):
        try:
            student = get_object_or_404(User, pk=student_id)
        except User.DoesNotExist:
            return HttpResponse("Студент с указанным ID не найден.", status=404)


        today = date.today()

        # Установка русской локали
        # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        # Получение названия месяца
        month_name = today.strftime("%B")

        today_str = f"{today.day} {month_name.capitalize()} {today.year} года"

        # Открытие сертификата в виде изображения с помощью PIL
        certificate_path = 'users/static/admin/img/certificate.png'  # Обновите путь к вашему сертификату
        certificate_image = Image.open(certificate_path)

        # Создание временного файла для сохранения сертификата
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filepath = temp_file.name
            certificate_image.save(temp_filepath, format='PNG')

        # Создание PDF-сертификата с помощью reportlab
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(A4))

        # Вставка сертификата как изображения на PDF-страницу
        p.drawImage(temp_filepath, 0, 0, width=850, height=600)

        # Вставка данных на сертификат

        # Установка шрифта
        font_path = 'users/static/fonts/Tinos-Italic.ttf'
        pdfmetrics.registerFont(TTFont('Tinos', font_path))

        # Расположение текста на сертификате
        text_x = 360  # Горизонтальная позиция текста
        text_y = 340  # Вертикальная позиция текста
        line_height = 20  # Высота строки

        # Вставка имени студента
        p.setFont("Tinos", 20)
        p.drawString(text_x, text_y, student.first_name)
        p.drawString(text_x + p.stringWidth(student.first_name) + 5, text_y, student.last_name)

        # Обновление вертикальной позиции для следующего текстового блока
        text_y -= line_height * 1

        # Вставка даты завершения курса
        date_text_x = 310  # Горизонтальная позиция текста даты
        date_text_y = 265  # Вертикальная позиция текста даты
        p.setFont("Tinos", 15)
        p.drawString(date_text_x, date_text_y, today_str)

        # Обновление вертикальной позиции для следующего текстового блока
        text_y -= line_height * 2


        text_course_x = 275
        text_course_y = 241

        # Вставка информации о курсе
        student = get_object_or_404(User, pk=student_id)
        course_names = student.courses.all().values_list('title', flat=True)
        course_text = f"{', '.join(course_names)}"  # Замените на фактическое название курса
        p.setFont("Tinos", 17)
        p.drawString(text_course_x, text_course_y, course_text)


        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')



