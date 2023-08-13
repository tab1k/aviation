from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from courses.models import Course, CourseType
from users.models import User, Stream


@login_required(login_url='users:login')
def curator_view(request):
    curator = request.user
    if request.user.role == 'curator':
        courses = Course.objects.all()
        courses_type = CourseType.objects.all()
        return render(request, 'users/curator/mainAfterSignUpСurator.html', {'courses': courses, 'courses_type': courses_type,
                                                                             'curator' : curator})
    else:
        return redirect('users:login')


class StudentsCheckAdmin(View):
    template_name = 'users/curator/student.html'

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


class StreamListView(ListView):
    model = Stream
    template_name = 'users/curator/streams.html'
    context_object_name = 'streams'


class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу



