from django import forms
from courses.models import Course
from users.models import User


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'courses']


class CuratorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'courses']
