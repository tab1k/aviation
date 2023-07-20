from django.shortcuts import render
from django.views import View
from courses.models import Course
from schedule.models import Schedule


class StudentScheduleView(View):
    template_name_student = 'users/student/timeTable.html'
    template_name_curator = 'users/curator/timeTableAdmin.html'
    template_name_admin = 'users/admin/timeTableAdmin.html'

    def get(self, request):
        # Получить текущего пользователя
        current_user = request.user

        # Определить тип пользователя
        user_role = current_user.role

        # Получить все курсы
        all_courses = Course.objects.all()

        # Определим дни недели
        weekdays = [
            ('Пн', 'Понедельник'),
            ('Вт', 'Вторник'),
            ('Ср', 'Среда'),
            ('Чт', 'Четверг'),
            ('Пт', 'Пятница'),
            ('Сб', 'Суббота'),
        ]

        # В зависимости от типа пользователя, выберем соответствующий шаблон
        if user_role == 'student':
            template_name = self.template_name_student
            # Получить расписание для курсов, на которых состоит текущий студент
            schedules = Schedule.objects.filter(course__students=current_user)
        elif user_role == 'curator':
            template_name = self.template_name_curator
            # TODO: Implement curator's schedules filtering if needed
            # Get the courses where the current_user is the curator
            courses_as_curator = Course.objects.filter(curators=current_user)

            # Get schedules for the courses where the current_user is the curator
            schedules = Schedule.objects.filter(course__in=courses_as_curator)
        else:
            template_name = self.template_name_admin
            # For admin, display all schedules regardless of the assigned students
            schedules = Schedule.objects.all()

        context = {
            'schedules': schedules,
            'weekdays': weekdays,
            'user_role': user_role,
            'all_courses': all_courses,
        }
        return render(request, template_name, context)




