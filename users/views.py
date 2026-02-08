from django_filters.rest_framework import ChoiceFilter, DjangoFilterBackend, FilterSet
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from users.models import Payment, Subscription, User
from lms.models import Course
from users.serializers import PaymentSerializer, SubscriptionSerializer, UserSerializer


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


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["post"])
    def create_subscription(self, request):
        # Получаем текущего пользователя
        user = request.user
        # Получаем ID курса из тела запроса
        course_id = request.data.get("course_id")
        
        # Получаем объект курса из базы данных
        course_item = get_object_or_404(Course, pk=course_id)
        
        # Проверяем наличие существующих подписок пользователя на этот курс
        subs_item = Subscription.objects.filter(user=user, course=course_item).first()
    
        # Если подписка у пользователя на этот курс есть - удаляем её
        if subs_item:
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаём новую подписку
        else:
            new_sub = Subscription.objects.create(user=user, course=course_item, is_subscription=True)
            message = 'подписка добавлена'
            
        # Возвращаем ответ в API
        return Response({"message": message}, status=status.HTTP_200_OK)
