from django.db import models
from django.contrib.auth.models import AbstractUser

from lms.models import Lesson, Сourse


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True, help_text='Введите номер телефона')
    sity = models.CharField(max_length=150, verbose_name='Город', blank=True, null=True, help_text='Введите город')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True, help_text='Загрузите аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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
    date_payment = models.DateField(
        verbose_name="Дата оплаты", 
        help_text="Укажите дату оплаты"
    )
    сourse = models.ForeignKey(
        Сourse,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    lesson = models.ForeignKey(
        Lesson,
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
