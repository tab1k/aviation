from django.shortcuts import render
from django.views import View
from courses.models import Course
from users.models import User
from django.views.generic import DetailView
from django.utils.timezone import localtime


class Profile(View):
    def get(self, request):
        user = User.objects.get(username=request.user.username)

        courses = Course.objects.all()

        context = {
            'user': user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'courses': courses
        }

        if user.role == 'student':
            courses = Course.objects.filter(students=user)
            return render(request, 'users/student/profileSettings.html', {'context': context, 'courses': courses})
        elif user.role == 'curator':
            courses = Course.objects.filter(curators=user)
            return render(request, 'users/curator/profileSettingsAdmin.html', {'context': context, 'courses': courses})
        elif user.role == 'admin':
            courses = Course.objects.all()
            return render(request, 'users/admin/profileSettingsAdmin.html', {'context': context, 'courses': courses})
        else:
            return render(request, 'users/404.html')



class ProfileView(DetailView):
    model = User
    template_name = 'users/admin/profileSettingsAdmin.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Проверка наличия файла перед его использованием
        if user.image:
            try:
                context['user_image_url'] = user.image.url
            except ValueError:
                # Обработка исключения, если файл некорректный
                context['user_image_url'] = None
        else:
            context['user_image_url'] = None

        # Добавление информации о последнем входе пользователя и его роли
        context['last_login'] = localtime(user.last_login)
        context['role'] = user.role

        # Получение списка курсов, в которых участвует студент
        courses = Course.objects.filter(students=user)
        context['courses'] = courses

        return context









