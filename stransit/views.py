import telebot
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from aviation import settings
from stransit.models import *


# Create your views here.


class GeneralView(View):
    def get(self, request):
        return render(request, 'users/stransit/index.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Сохранение данных в базе данных
        contact = Contact(name=name, email=email, phone_number=phone_number, message=message)
        contact.save()

        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        message_text = f"❕Новая заявка❕\n\n⚜️Имя:{name}.\n\n⚜️Email: {email}\n\n⚜️Телефон: {phone_number}\n\n⚜️Сообщение: {message}"
        bot.send_message(chat_id, message_text)

        return render(request, 'users/stransit/index.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'users/stransit/about.html')



class CoursesView(View):

    def get(self, request):
        return render(request, 'users/stransit/all_courses.html')



class OnlineCoursesView(View):

    template_name  = 'users/stransit/online_courses.html'
    online_courses = OnlineCourses.objects.all()

    def get(self, request):

        return render(request, self.template_name, {
            'online' : self.online_courses,
        })


class IndustrialCourse(View):
    template_name = 'users/stransit/industrial_course.html'
    items_per_page = 8  # Количество элементов на странице

    def get(self, request):
        industrial_courses = IndustrialCourses.objects.order_by('id').all()

        paginator = Paginator(industrial_courses, self.items_per_page)
        page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра

        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'industrial': page_obj,
            'has_previous': page_obj.has_previous(),
            'previous_page_url': request.path + '?page=' + str(
                page_obj.previous_page_number()) if page_obj.has_previous() else '',
            'has_next': page_obj.has_next(),
            'next_page_url': request.path + '?page=' + str(page_obj.next_page_number()) if page_obj.has_next() else '',
            'page_range': paginator.page_range,
            'current_page': page_obj.number,
            'page_url': ' '.join([request.path + '?page=' + str(page) for page in paginator.page_range]),
        })


class AviationCourse(View):
    template_name = 'users/stransit/aviation_course.html'
    items_per_page = 8  # Количество элементов на странице

    def get(self, request):
        aviation_courses = AviationCourses.objects.all()

        paginator = Paginator(aviation_courses, self.items_per_page)
        page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра

        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'aviation': page_obj,
            'page_number': page_number,
            'has_previous': page_obj.has_previous(),
            'previous_page_url': f'?page={page_obj.previous_page_number()}' if page_obj.has_previous() else None,
            'has_next': page_obj.has_next(),
            'next_page_url': f'?page={page_obj.next_page_number()}' if page_obj.has_next() else None,
            'page_range': paginator.page_range,
            'current_page': page_obj.number,
        })



class CertificatesView(View):

    def get(self, request):
        return render(request, 'users/stransit/certificates.html')



class ContactsView(View):

    def get(self, request):
        return render(request, 'users/stransit/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Сохранение данных в базе данных
        contact = Contact(name=name, email=email, phone_number=phone_number, message=message)
        contact.save()

        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        message_text = f"❕Новая заявка❕\n\n⚜️Имя:{name}.\n\n⚜️Email: {email}\n\n⚜️Телефон: {phone_number}\n\n⚜️Сообщение: {message}"
        bot.send_message(chat_id, message_text)

        return render(request, 'users/stransit/index.html')

