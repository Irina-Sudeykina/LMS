from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_information_update_course(email_list, title):
    send_mail(
        subject="Обновление!",
        message=f"Курс {title} обновлен.",
        from_email=EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=False,
    )
    print("Письма отправлены.", title)


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
