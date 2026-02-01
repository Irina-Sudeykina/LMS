from django.db import models
# from users.models import User


class Сourse(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(
        upload_to="сourse/image", blank=True, null=True, verbose_name="Превью", help_text="Загрузите превью курса"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owned_courses",
        verbose_name="Владелец", 
        help_text="Укажите владельца курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lesson/image", blank=True, null=True, verbose_name="Превью", help_text="Загрузите превью урока"
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите URL видео (например, YouTube)",
    )
    сourse = models.ForeignKey(
        Сourse,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Введите курс",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owned_lessons",
        verbose_name="Владелец", 
        help_text="Укажите владельца урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["сourse", "title"]

    def __str__(self):
        return f"{self.сourse}: {self.title}"
