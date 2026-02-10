from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner")
    list_filter = ("title", "description", "owner")
    search_fields = ("title", "description", "owner")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "course", "owner")
    list_filter = ("title", "description", "course", "owner")
    search_fields = ("title", "description", "course", "owner")
