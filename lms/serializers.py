from rest_framework import serializers

from lms.models import Lesson, Сourse


class СourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Сourse
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
