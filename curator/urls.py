from django.urls import path, include
from curator.views import *

app_name = 'curator'

urlpatterns = [
    path('', curator_view, name='curator'),
    path('previous/<int:lesson_id>/', show_previous_lesson, name='previous_lesson'),
    path('next/<int:lesson_id>/', show_next_lesson, name='next_lesson'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('curator_check/students/', StudentsCheckAdmin.as_view(), name='students_admin_check'),
    path('streams/', StreamListView.as_view(), name='stream_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Другие пути для пользователей...
]
