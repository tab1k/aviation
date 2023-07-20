from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.utils.timezone import localtime, now
from django.http import JsonResponse
from comments.forms import CommentForm
from comments.models import Comment
from .models import Course, Module, CourseType, Lesson


# Представление для отображения типов курсов
class CoursesByType(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, type_id):
        # Получаем тип курса по type_id
        course_type = get_object_or_404(CourseType, id=type_id)

        # Получаем все курсы, относящиеся к данному типу курса и в которых студент присутствует
        courses = course_type.courses.filter(students=request.user)

        # Получаем уникальные типы курсов, связанные с курсами, в которых студент присутствует
        related_course_types = CourseType.objects.filter(courses__students=request.user).distinct()

        # Определение шаблона в зависимости от роли пользователя
        if request.user.groups.filter(name='Студенты').exists():
            template_name = 'users/student/courses_by_type.html'
        elif request.user.groups.filter(name='Кураторы').exists():
            template_name = 'users/curator/courses_by_type.html'
        elif request.user.groups.filter(name='Администраторы').exists():
            template_name = 'users/admin/courses_by_type.html'
        else:
            # Если пользователь не принадлежит ни к одной из групп или не аутентифицирован, перенаправляем его на страницу входа
            return redirect('users:login')

        return render(request, template_name, {'course_type': course_type, 'courses': courses, 'related_course_types': related_course_types})


class Courses(View):

    def get(self, request):
        if request.user.groups.filter(name='Администраторы').exists():
            template_name = 'users/admin/coursesAfterSignUpAdmin.html'
            courses = Course.objects.all()
        elif request.user.groups.filter(name='Кураторы').exists():
            template_name = 'users/curator/coursesAfterSignUpCurator.html'
            courses = Course.objects.filter(curators=request.user)
        else:
            template_name = 'users/student/coursesAfterSignUp.html'
            courses = Course.objects.filter(students=request.user)

        # Get all comments (both student and curator comments) for the current user
        all_comments = Comment.objects.filter(Q(user=request.user) | Q(curator=request.user))

        # Separate student and curator comments
        student_comments = all_comments.filter(is_student_comment=True)
        curator_comments = all_comments.filter(is_student_comment=False)

        # Get the current date and time in the Asia/Almaty timezone
        current_time = localtime(now())

        return render(request, template_name, {
            'courses': courses,
            'current_time': current_time,
            'student_comments': student_comments,
            'curator_comments': curator_comments
        })


# Представление для отображения Модулей
class Modules(View):

    def get(self, request, pk):

        if request.user.groups.filter(name='Администраторы').exists():
            module = Module.objects.filter(course__pk=pk)
            return render(request, 'users/admin/module.html', {'modules': module})

        elif request.user.groups.filter(name='Кураторы').exists():
            module = Module.objects.filter(course__pk=pk, course__curators=request.user)
            return render(request, 'users/curator/moduleAdmin.html', {'modules': module})

        else:
            module = Module.objects.filter(course__pk=pk, course__students=request.user)
            return render(request, 'users/student/module.html', {'modules': module})


# Представление для отображения
class CourseDetailView(View):

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return render(request, 'users/admin/detail.html', {'course': course})


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


# Представление для отображения урока

class LessonView(View):
    student_template = 'users/student/video.html'
    curator_template = 'users/curator/videoAdmin.html'
    admin_template = 'users/admin/videoAdmin.html'

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        module = lesson.module
        lessons = Lesson.objects.filter(module=module)
        comment_form = CommentForm()
        student_comments = Comment.objects.filter(lesson=lesson,
                                                  is_student_comment=True)  # Получаем комментарии студентов

        if request.user.role == 'student':
            return render(request, self.student_template,
                          {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form,
                           'student_comments': student_comments})  # Включаем student_comments в контекст
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


class AnswersView(View):
    template_curator = 'users/curator/answers.html'
    template_admin = 'users/admin/answers.html'
    template_error = 'users/404.html'

    def get(self, request):
        student_comments = Comment.objects.filter(is_student_comment=True)

        if request.user.role == 'curator':
            template_name = self.template_curator
        elif request.user.role == 'admin':
            template_name = self.template_admin
        else:
            template_name = self.template_error

        return render(request, template_name, {'comments': student_comments})

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
            return render(request, 'users/404.html')  # Здесь используем перенаправление для студентов, но вы можете выбрать другой путь





