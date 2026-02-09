from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Python разработчик", description="Очень интересная профессия")
        self.lesson = Lesson.objects.create(title="Валидаторы", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get("title"),
            self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "Пагинация",
            "course": self.course.id,    # Добавляем ссылку на курс
            "owner": self.user.id        # Добавляем владельца
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "Пагинация"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get("title"), "Пагинация"
        )

    def test_lesson_delete(self):
        url = reverse("lms:lesson_detete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

        data = response.json()

        result = {
            'count': 1, 
            'next': None, 
            'previous': None, 
            'results': [{
                'id': self.lesson.pk, 
                'video_url': None, 
                'title': self.lesson.title, 
                'description': None, 
                'preview': None, 
                'course': self.course.pk, 
                'owner': self.user.pk
            }]
        }

        self.assertEqual(
            data,
            result
        )
