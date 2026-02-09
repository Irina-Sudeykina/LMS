from rest_framework.routers import SimpleRouter

from users.views import SubscriptionViewSet

app_name = "subscriptions"

router = SimpleRouter()
router.register(r"", SubscriptionViewSet, basename="subscriptions")

urlpatterns = router.urls
