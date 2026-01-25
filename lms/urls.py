from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView, LessonRetrieveAPIView,
                       LessonUpdateAPIView, СourseViewSet)

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r"courses", СourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_detete"),
] + router.urls
