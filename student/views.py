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



from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Lesson

def show_previous_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, pk=lesson_id)
    all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('id')

    current_lesson_index = None
    for index, lesson in enumerate(all_lessons):
        if lesson.id == current_lesson.id:
            current_lesson_index = index
            break

    if current_lesson_index is not None and current_lesson_index > 0:
        previous_lesson = all_lessons[current_lesson_index - 1]
        return redirect('users:student:previous_lesson', lesson_id=previous_lesson.id)
    else:
        return redirect('users:student:courses:lesson_view', lesson_id=current_lesson.id)


def show_next_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, pk=lesson_id)
    all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('id')

    current_lesson_index = None
    for index, lesson in enumerate(all_lessons):
        if lesson.id == current_lesson.id:
            current_lesson_index = index
            break

    if current_lesson_index is not None and current_lesson_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_lesson_index + 1]
        return redirect('users:student:next_lesson', lesson_id=next_lesson.id)
    else:
        return redirect('users:student:courses:lesson_view', lesson_id=current_lesson.id)




class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
