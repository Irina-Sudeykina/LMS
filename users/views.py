from django_filters.rest_framework import ChoiceFilter, DjangoFilterBackend, FilterSet
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from users.models import Payment, Subscription, User
from lms.models import Course, Lesson
from users.serializers import PaymentSerializer, SubscriptionSerializer, UserSerializer
from users.servises import create_stripe_product, create_stripe_price, create_stripe_sessions


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action in ("create"):
            self.permission_classes = (AllowAny,)
        return super().get_permissions()


class PaymentFilter(FilterSet):
    """
    Настроим точный фильтр по способу оплаты.
    Определяем жестко допустимые методы оплаты.
    """

    method = ChoiceFilter(field_name="method", lookup_expr="exact", choices=Payment.METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "method"]


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter  # Применяем кастомный фильтр
    ordering_fields = ("date_payment",)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Передаем текущего пользователя в сериализатор
        serializer.save(user=self.request.user)
        payment = serializer.instance

        # Формируем заголовок продукта
        if payment.course:
            title = f"Курс: {payment.course.title}"
        elif payment.lesson:
            title = f"Лекция: {payment.lesson.title}"
        else:
            # Установим дефолтное название, если ничего не выбрано
            title = "Оплата сервиса"

        # Создание продукта и цены в Stripe
        product = create_stripe_product(title)
        price = create_stripe_price(product, payment.amount)
        session_id, payment_link = create_stripe_sessions(price)

        # Сохраняем ID сессии и ссылку на оплату
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)

    # def perform_create(self, serializer):
        # Получаем текущего пользователя
        # user = self.request.user
        # Получаем объект курса из сериализатора
        # course = serializer.validated_data.get('course')
        
        # Проверяем наличие существующих подписок
        # existing_subs = Subscription.objects.filter(user=user, course=course)
        
        # if existing_subs.exists():
            # Если подписки есть, удаляем их все
            # existing_subs.delete()
        # else:
            # Если подписки нет, создаем новую
            # serializer.save()
