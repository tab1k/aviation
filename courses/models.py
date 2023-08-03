from django.contrib.auth import get_user_model
from django.db import models
from users.models import User
from embed_video.fields import EmbedVideoField


class CourseType(models.Model):
    title = models.CharField(max_length=155, null=True, blank=True)
    description = models.CharField(max_length=155, null=True, blank=True)
    time = models.PositiveIntegerField(default=90, null=True, blank=True)
    photo = models.ImageField(upload_to='course_type_images', null=True, blank=True)

    def __str__(self):
        return self.title

    def has_courses_with_curators(self, user):
        return self.courses.filter(curators=user).exists()

    class Meta:
        verbose_name = 'Тип курса'
        verbose_name_plural = 'Типы курсов'


class Course(models.Model):
    title = models.CharField(max_length=255)  # Название курса
    description = models.TextField()  # Описание курса
    duration = models.PositiveIntegerField()  # Продолжительность курса
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses') # Связь с моделью "Course Type"
    curators = models.ManyToManyField(get_user_model())   # Связь с моделью "Curator"
    students = models.ManyToManyField(User, related_name='courses', blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Module(models.Model):
    title = models.CharField(max_length=255)  # Название модуля
    description = models.TextField()  # Описание модуля
    order = models.PositiveIntegerField()  # Порядковый номер модуля
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')  # Связь с моделью "Course"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


class Lesson(models.Model):
    title = models.CharField(max_length=255)  # Название урока
    description = models.TextField()  # Описание урока
    video = EmbedVideoField() # Видео
    zoom_link = models.URLField(blank=True, null=True)
    learn_documentation = models.FileField(blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)  # Связь с моделью "Module"


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


