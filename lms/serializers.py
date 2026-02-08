from rest_framework import serializers

from lms.models import Lesson, Course
from lms.validators import validate_url_source


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_url_source])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
