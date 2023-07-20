from django.db import models

from courses.models import Lesson
from users.models import User


class Essay(models.Model):
    text = models.TextField()  # Текст эссе
    files = models.FileField(upload_to='essays/')  # Файлы эссе
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Связь с моделью "User"

    def __str__(self):
        return f'Эссе под {self.lesson} от {self.user}'

    class Meta:
        verbose_name = 'Эссе'
        verbose_name_plural = 'Эссе'


class EssayResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с моделью "User"
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"
    essay_text = models.TextField()  # Текст эссе
    is_passed = models.BooleanField(default=False)  # Флаг, указывающий, прошел ли студент эссе

    def __str__(self):
        return f"Essay Result: {self.student.username} - {self.lesson.title}"

    class Meta:
        verbose_name = 'Результат эссе'
        verbose_name_plural = 'Результаты эссе'