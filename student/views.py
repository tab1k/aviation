from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View

import courses
from courses.models import *
from users.models import *


@login_required(login_url='users:login')
def dashboard_view(request):
    student = request.user
    course_type = CourseType.objects.filter(courses__students=student).distinct()
    courses = Course.objects.filter(students=student)
    if request.user.role == 'student':
        return render(request, 'users/student/mainAfterSignupStudent.html', {'courses': courses,
                                                                             'course_type' : course_type,
                                                                             'student': student})
    else:
        return redirect('users:login')




def back_to_home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('users:admin:admin')  # Замените 'admin_home' на имя URL-шаблона главной страницы администратора
        elif request.user.role == 'curator':
            return redirect('users:curator:curator')  # Замените 'curator_home' на имя URL-шаблона главной страницы куратора
        else:
            return redirect('users:student:student')  # Замените 'student_home' на имя URL-шаблона главной страницы студента
    else:
        return redirect('login')  # Замените 'login' на имя URL-шаблона страницы входа


class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('stransit:users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
