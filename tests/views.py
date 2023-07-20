from random import random
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Test, TestChoice, TestResult
from courses.models import Lesson
from users.models import User


class DoTest(View):

    student_template = 'users/student/test.html'
    curator_template = 'users/curator/testAdmin.html'
    admin_template = 'users/admin/testAdmin.html'

    def get(self, request):

        if request.user.role == 'student':
                return render(request, self.student_template)
        elif request.user.role == 'curator':
            return render(request, self.curator_template)
        elif request.user.role == 'admin':
            return render(request, self.admin_template)
        else:
            return render(request, 'users/404.html')

