from django_filters.rest_framework import ChoiceFilter, DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentFilter(FilterSet):
    """
    Настроим точный фильтр по способу оплаты.
    Определяем жестко допустимые методы оплаты.
    """

    method = ChoiceFilter(field_name="method", lookup_expr="exact", choices=Payment.METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ["сourse", "lesson", "method"]


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter  # Применяем кастомный фильтр
    ordering_fields = ("date_payment",)
