from django.urls import path, include
from student.views import dashboard_view, LogoutView

app_name = 'student'

urlpatterns = [
    path('', dashboard_view, name='student'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Другие пути для пользователей...
]


