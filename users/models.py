from django.contrib.auth.models import AbstractUser
from django.db import models

# from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона"
    )
    sity = models.CharField(max_length=150, verbose_name="Город", blank=True, null=True, help_text="Введите город")
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    METHOD_CHOICES = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Введите пользователя",
    )
    date_payment = models.DateField(verbose_name="Дата оплаты", help_text="Укажите дату оплаты")
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Урок",
        help_text="Выберите урок",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", help_text="Введите сумму оплаты")
    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default="transfer",
        editable=False,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="id сессии",
        blank=True,
        null=True,
        help_text="Введите id сессии",
    )
    link = models.URLField(
        max_length=800,
        verbose_name="Ссылка на оплату",
        blank=True,
        null=True,
        help_text="Введите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.date_payment} - {self.user}: {self.amount}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
        help_text="Введите пользователя",
    )
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subscriptions",
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    is_subscription = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user}: {self.course} - {self.is_subscription}"
