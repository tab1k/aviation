from django.urls import path, include
from curator.views import curator_view, StudentsCheckAdmin, LogoutView

app_name = 'curator'

urlpatterns = [
    path('', curator_view, name='curator'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls')),
    path('schedule/', include('schedule.urls')),
    path('curator_check/students/', StudentsCheckAdmin.as_view(), name='students_admin_check'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Другие пути для пользователей...
]
