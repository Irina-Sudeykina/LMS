from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import PaymentViewSet

app_name = 'payments'

router = SimpleRouter()
router.register(r"", PaymentViewSet, basename="payments")

urlpatterns = router.urls