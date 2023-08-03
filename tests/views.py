from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from courses.models import Lesson
from essays.models import EssaySubmission
from users.models import User
from .models import Test, TestChoice, TestResult


class TakeTestView(View):
    template_name = 'users/student/test.html'

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        questions = Test.objects.filter(lesson=lesson)
        context = {
            'lesson': lesson,
            'questions': questions,
        }
        return render(request, self.template_name, context)

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        questions = Test.objects.filter(lesson=lesson)
        user = request.user

        total_score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = TestChoice.objects.get(pk=selected_choice_id)
            if selected_choice.is_correct:
                total_score += selected_choice.score

        test_result, created = TestResult.objects.get_or_create(student=user, lesson=lesson)
        test_result.score = total_score
        test_result.save()

        return redirect('stransit:users:student:courses:tests:test_result', lesson_id=lesson_id)



class TestResultView(View):
    template_name = 'users/student/test_result.html'

    def get(self, request, lesson_id):
        current_user = request.user
        lesson = get_object_or_404(Lesson, pk=lesson_id)

        if not (current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser or current_user.role in ['student', 'curator', 'admin'])):
            messages.warning(request, "У вас нет доступа к результатам теста.")
            return redirect('users:student:courses:tests:take_test', lesson_id=lesson_id)

        test_results = TestResult.objects.filter(student=current_user, lesson=lesson)

        total_questions = Test.objects.filter(lesson=lesson).count()
        total_correct_answers = sum(result.score for result in test_results if result.score is not None)

        # Предположим, что значение total_possible_score уже известно (например, 100)
        total_possible_score = 100

        # Calculate if total_score is greater than or equal to half of total_possible_score
        is_passing_grade = total_correct_answers >= total_possible_score / 2

        # Получаем список вопросов теста
        test_questions = Test.objects.filter(lesson=lesson)

        # Check if essay is allowed (assuming you have the logic for it)
        essay_allowed = True  # Replace this with your actual logic

        context = {
            'lesson': lesson,
            'test_results': test_results,
            'total_score': total_correct_answers,
            'total_questions': total_questions,
            'total_possible_score': total_possible_score,
            'is_passing_grade': is_passing_grade,
            'essay_allowed': essay_allowed,
            'test_questions': test_questions,
        }

        return render(request, 'users/student/test_result.html', context)








 # student_template = 'users/student/test.html'
 #    curator_template = 'users/curator/testAdmin.html'
 #    admin_template = 'users/admin/testAdmin.html'