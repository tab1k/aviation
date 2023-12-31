from django.urls import path
from stransit.views import *

app_name = 'stransit'

urlpatterns = [
    path('', GeneralView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('courses', CoursesView.as_view(), name='all_courses'),
    path('online_courses', OnlineCoursesView.as_view(), name='online_courses'),
    path('industrial_course/', IndustrialCourse.as_view(), name='industrial_course'),
    path('industrial_course/page/<int:page>/', IndustrialCourse.as_view(), name='industrial_course_paginated'),
    path('aviation_course', AviationCourse.as_view(), name='aviation_course'),
    path('aviation_course/page/<int:page>/', AviationCourse.as_view(), name='aviation_course_paginated'),
    path('partners', CertificatesView.as_view(), name='certificates'),
    path('contacts', ContactsView.as_view(), name='contacts'),
]
