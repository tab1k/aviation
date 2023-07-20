from django.urls import path, include
from users.views import back_to_home, login_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', include('administrator.urls', namespace='admin')),
    path('student/', include('student.urls', namespace='student')),
    path('curator/', include('curator.urls', namespace='curator')),
    path('back-to-home/', back_to_home, name='back_to_home'),
]




# import curator.views
# import student.views
# from courses.views import Courses

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('admin/', views.admin_view, name='admin'),
#     path('dashboard/', include('student.urls', namespace='dashboard')),
#     path('curator/', include('curator.urls', namespace='curator')),
#
#     # Другие пути для пользователей...
# ]


# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('dashboard/', dashboard_view, name='dashboard'),
#     path('curator/', curator_view, name='curator'),
#     path('admin/', views.admin_view, name='admin'),
#     # Другие пути для пользователей...
# ]