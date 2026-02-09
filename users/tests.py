from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Python разработчик", description="Очень интересная профессия")
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_retrieve(self):
        url = reverse("subscriptions:subscriptions-detail", kwargs={"pk": self.subscription.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscription.objects.all().count(), 1
        )

    def test_subscription_create(self):
        url = reverse("subscriptions:subscriptions-list")
        data = {
            "course_id": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(), 0
        )
        print(response.json())
