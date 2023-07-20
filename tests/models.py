from django.db import models
from courses.models import Lesson
from users.models import User


class Test(models.Model):
    question = models.TextField()  # Вопрос
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Связь с моделью "User"
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Тестовый вопрос'
        verbose_name_plural = 'Тестовые вопросы'


class TestChoice(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  # Связь с моделью "Test"
    choice = models.CharField(max_length=255)  # Вариант ответа
    is_correct = models.BooleanField(default=False)  # Правильный ответ

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с моделью "User"
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"
    score = models.PositiveIntegerField()  # Оценка

    def __str__(self):
        return f"Test Result: {self.student.username} - {self.lesson.title}"

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

