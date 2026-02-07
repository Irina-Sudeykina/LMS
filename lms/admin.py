from django.contrib import admin

from .models import Lesson, Сourse


@admin.register(Сourse)
class СourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner")
    list_filter = ("title", "description", "owner")
    search_fields = ("title", "description", "owner")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "сourse", "owner")
    list_filter = ("title", "description", "сourse", "owner")
    search_fields = ("title", "description", "сourse", "owner")
