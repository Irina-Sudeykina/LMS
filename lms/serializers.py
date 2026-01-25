from rest_framework import serializers

from lms.models import Lesson, Сourse


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class СourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, course):
        return course.lessons.count()

    class Meta:
        model = Сourse
        fields = "__all__"
