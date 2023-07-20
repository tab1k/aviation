from django.contrib import admin
from courses.models import Course, Module, Lesson, CourseType



class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'time')  # Замените 'duration' и 'category' на существующие поля модели CourseType



class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'course_type')
    search_fields = ('title', 'course_type')


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'video')
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title', 'module__course__title')

admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)


