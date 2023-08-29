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
    path('applications/', ContactListView.as_view(), name='admin_applications'),
    path('view-notifications/', NotificationListView.as_view(), name='view_notifications'),
    path('view-notifications/course/<int:course_id>/', NotificationListView.as_view(), name='view_notifications_by_course'),
    path('create-notification/', NotificationCreateView.as_view(), name='create_notification'),
    path('search/', SearchView.as_view(), name='search'),
    # Другие пути для пользователей...
]
