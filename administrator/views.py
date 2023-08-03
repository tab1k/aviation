from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import logout, get_user_model
from django.db.models import Q
from administrator.forms import StudentForm, CuratorForm
from courses.models import Course, CourseType
from users.models import User, Stream
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model


@login_required(login_url='users:login')
def admin_view(request):
    admin = request.user
    if request.user.role == 'admin':
        courses = Course.objects.all()
        courses_type = CourseType.objects.all()
        return render(request, 'users/admin/mainAfterSignUpAdmin.html', {'courses': courses, 'courses_type': courses_type, 'admin' : admin})
    else:
        return redirect('users:login')


class StudentsCheckAdmin(View):
    template_name = 'users/admin/student.html'

    def get(self, request, stream_id=None):
        streams = Stream.objects.all()
        selected_stream = None
        students = User.objects.filter(role='student')

        if stream_id:
            selected_stream = get_object_or_404(Stream, id=stream_id)
            students = students.filter(stream=selected_stream)

        return render(request, self.template_name, {
            'students': students,
            'streams': streams,
            'selected_stream': selected_stream
        })


class CuratorCheckAdmin(View):
    template_name = 'users/admin/curators.html'

    def get(self, request):
        curators = User.objects.filter(role='curator')
        return render(request, self.template_name, {'curators' : curators})


class AddStudent(View):
    template_name = 'users/admin/addstudent.html'

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            student = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role='student'
            )
            courses = form.cleaned_data['courses']
            student.courses.set(courses)

            # Добавляем студента в группу 'Студенты'
            student_group = Group.objects.get(name='Студенты')
            student.groups.add(student_group)

            return redirect('users:admin:courses:detail', course_id=courses.first().id)
        return render(request, self.template_name, {'form': form})


class AddCurator(View):
    template_name = 'users/admin/addCoach.html'

    def get(self, request):
        form = CuratorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CuratorForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            curator = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role='curator'
            )
            courses = form.cleaned_data['courses']
            curator.courses.set(courses)

            # Добавляем куратора в группу 'Кураторы'
            curator_group = Group.objects.get(name='Кураторы')
            curator.groups.add(curator_group)

            return redirect('users:admin:courses:detail', course_id=courses.first().id)
        return render(request, self.template_name, {'form': form})


class SearchStudentsView(View):
    def get_template_names(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Если поле role у пользователя равно "admin", используем шаблон для администратора
        if user.role == 'admin':
            return ['users/admin/student.html']
        # Иначе используем шаблон для куратора
        else:
            return ['users/curator/student.html']

    def get(self, request):
        query = request.GET.get('q')
        stream = request.GET.get('stream')

        students = User.objects.filter(
            role='student',
            first_name__icontains=query,
        )

        if stream:
            students = students.filter(stream__number=int(stream))

        context = {'students': students}
        return render(request, self.get_template_names(), context)



class SearchCuratorsView(View):
    template_name = 'users/admin/curators.html'

    def get(self, request):
        query = request.GET.get('q')
        stream = request.GET.get('stream')

        curators = User.objects.filter(role='curator')

        if query:
            curators = curators.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if stream:
            curators = curators.filter(stream__number=int(stream))

        context = {'results': curators}
        return render(request, self.template_name, context)





class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('stransit:index')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
