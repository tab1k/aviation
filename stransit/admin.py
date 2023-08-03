from django.contrib import admin
from stransit.models import *


class IndustrialCoursesAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'about_course', 'photo')
    list_filter = ('title', 'type')
    search_fields = ('title', 'type')


class AviationCoursesAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'about_course', 'photo')
    list_filter = ('title', 'type')
    search_fields = ('title', 'type')


class OnlineCoursesAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'about_course', 'photo')
    list_filter = ('title', 'type')
    search_fields = ('title', 'type')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message')
    list_filter = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')


admin.site.register(IndustrialCourses, IndustrialCoursesAdmin)
admin.site.register(AviationCourses, AviationCoursesAdmin)
admin.site.register(OnlineCourses, OnlineCoursesAdmin)
admin.site.register(Contact, ContactAdmin)