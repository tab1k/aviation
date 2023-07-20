from django.contrib import admin
from essays.models import Essay


class EssayAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'text')
    list_filter = ('lesson',)
    search_fields = ('text', 'lesson__title')


admin.site.register(Essay, EssayAdmin)
