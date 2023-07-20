from django.urls import path, include
from administrator.views import *
from administrator.views import CuratorCheckAdmin
from administrator.views import StudentsCheckAdmin

app_name = 'admin'

urlpatterns = [
    path('', admin_view, name='admin'),
    path('add_student/', AddStudent.as_view(), name='add_student'),
    path('add_сurator/', AddCurator.as_view(), name='add_curator'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('admin_check/students/', StudentsCheckAdmin.as_view(), name='students_admin_check'),
    path('admin_check/students/search/', SearchStudentsView.as_view(), name='search_students'),
    path('admin_check/curators/', CuratorCheckAdmin.as_view(), name='curators_admin_check'),
    path('admin_check/curators/search/', SearchCuratorsView.as_view(), name='search_curators'),
]
