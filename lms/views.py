import datetime

from django.utils.timezone import now
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.paginators import CastomPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_information_update_course
from users.models import Subscription
from users.permissions import IsModer, isOwner


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CastomPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, updated_at=datetime.datetime.now())

    def perform_update(self, serializer):
        course = serializer.save()

        # Получить всех пользователей, подписанных на курс
        subscribed_users = Subscription.objects.filter(course=course, is_subscription=True)
        emails = []
        for subscription in subscribed_users:
            emails.append(subscription.user.email)

        # Отправить уведомление о смене курса пользователям
        send_information_update_course.delay(emails, course.title)

        # Обновить время изменения курса
        course.updated_at = now()
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | isOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | isOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        # Сохраняем новый урок с владельцем
        lesson = serializer.save(owner=self.request.user)

        # Получаем связанный курс и обновляем его поле updated_at
        course = lesson.course
        if course:
            # Получить всех пользователей, подписанных на курс
            subscribed_users = Subscription.objects.filter(course=course, is_subscription=True)
            emails = []
            for subscription in subscribed_users:
                emails.append(subscription.user.email)

            # Отправить уведомление о смене курса пользователям
            send_information_update_course.delay(emails, course.title)
            # Обновить время изменения курса
            course.updated_at = datetime.datetime.now()
            course.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CastomPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | isOwner)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | isOwner)

    def perform_update(self, serializer):
        # Выполняем основное обновление урока
        lesson = serializer.save()

        # Проверяем наличие связанного курса и обновляем его поле updated_at
        if lesson.course:
            # Получить всех пользователей, подписанных на курс
            subscribed_users = Subscription.objects.filter(course=lesson.course, is_subscription=True)
            emails = []
            for subscription in subscribed_users:
                emails.append(subscription.user.email)

            # Отправить уведомление о смене курса пользователям
            send_information_update_course.delay(emails, lesson.course.title)

            # Обновить время изменения курса
            lesson.course.updated_at = now()
            lesson.course.save(update_fields=["updated_at"])


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer | isOwner)
