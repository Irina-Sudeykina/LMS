from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="testadmin@mail.ru")
        user.set_password("1234")
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Success created admin user with email {user.email}"))
