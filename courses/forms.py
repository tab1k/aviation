from comments.models import Comment
from .models import Lesson, CourseType
from .models import Module
from django import forms
from courses.models import Course


class CourseTypeForm(forms.ModelForm):
    class Meta:
        model = CourseType
        fields = ['title', 'description', 'time', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course type title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter description'}),
            'time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in minutes'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding additional CSS classes (this is optional since already added in widgets)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['time'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control-file'})


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'image', 'course_type', 'curators', 'students']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter course description'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in minutes'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'curators': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding additional CSS classes and configurations if needed
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['course_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['curators'].widget.attrs.update({'class': 'form-control'})
        self.fields['students'].widget.attrs.update({'class': 'form-control'})

        # Placeholder to help admins understand they can search and select multiple students
        self.fields['students'].help_text = "You can select multiple students. Use the search bar for convenience."


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'course']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control select2'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'zoom_link', 'start_datetime', 'video', 'learn_documentation', 'module']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lesson title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter lesson description'}),
            'zoom_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Zoom link'}),
            'start_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter video link'}),
            'learn_documentation': forms.FileInput(attrs={'class': 'form-control-file'}),
            'module': forms.Select(attrs={'class': 'form-control select2'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
