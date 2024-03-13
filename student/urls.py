from django.urls import path, include
from student.views import *

app_name = 'student'

urlpatterns = [
    path('', dashboard_view, name='student'),
    path('lesson/<int:pk>/previous/', PreviousLessonRedirectView.as_view(), name='previous_lesson_redirect'),
    path('lesson/<int:pk>/next/', NextLessonRedirectView.as_view(), name='next_lesson_redirect'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('notifications/', StudentNotificationListView.as_view(), name='student_notifications'),
    path('messages/', StudentMessagesListView.as_view(), name='student_messages'),
    path('send_response/<int:comment_id>/', SendResponseView.as_view(), name='send_response'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Другие пути для пользователей...
]


