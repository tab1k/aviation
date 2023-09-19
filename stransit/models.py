from django.utils import timezone

from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    phone_number = models.BigIntegerField(blank=False, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новая заявка'
        verbose_name_plural = 'Новые заявки'




class StransitCourse(models.Model):

    LESSON_TYPE = (
        ('online', 'Онлайн курс'),
        ('industrial', 'Промышленный курс'),
        ('aviation', 'Авиационный курс'),
    )

    photo = models.ImageField(blank=True, null=True, upload_to='stransit_course_images', verbose_name='Фото')
    type = models.CharField(max_length=10,choices=LESSON_TYPE, blank=True, null=True, default='offline', verbose_name='Формат обучения')
    title = models.CharField(max_length=255, verbose_name='Название курса')
    about_course = models.TextField(max_length=300, verbose_name='О курсе')

    class Meta:
        abstract = True  # Указываем, что это абстрактный класс

# Теперь определяем ваши модели, наследующие от абстрактного класса Course:

class IndustrialCourses(StransitCourse):
    pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Промышленный курс'
        verbose_name_plural = 'Промышленные курсы'


class AviationCourses(StransitCourse):
    pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Авиционный курс'
        verbose_name_plural = 'Авиационные курсы'

class OnlineCourses(StransitCourse):
    pass

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Онлайн курс'
        verbose_name_plural = 'Онлайн курсы'