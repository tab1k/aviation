from django.urls import path
from .views import *

app_name = 'tests'

urlpatterns = [
    path('', DoTest.as_view(), name='tests'),
]