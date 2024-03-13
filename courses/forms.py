from django import forms
from comments.models import Comment
from courses.models import *


class LessonCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Название урока'}),
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4}),
        required=False
    )

    zoom_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ссылка на Zoom'}),
        required=False
    )

    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Дата и время начала'}),
        required=False
    )

    video = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ссылка на видео'}),
        required=False
    )

    learn_documentation = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        required=False
    )

    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        required=True,
        empty_label=None,
    )

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'zoom_link', 'start_datetime', 'video', 'learn_documentation', 'module']


class CourseCreationForm(forms.ModelForm):

    course_type = forms.ModelChoiceField(
        queryset=CourseType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg',
                                   'placeholder': 'Тип курса'}),
        required=True,
        empty_label=None,

    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                      'placeholder': 'Название курса'}),
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4,
                                     'placeholder': 'Описание курса'}),
        required=False
    )

    duration = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 1,
                                     'placeholder': 'Продолжительность курса'}),
        required=False
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg',
                                               'placeholder': 'Изображение курса'}),
        required=False
    )


    class Meta:
        model = Lesson
        fields = ['course_type', 'title', 'description', 'duration', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
