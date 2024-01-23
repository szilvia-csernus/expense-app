import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        try:
            User = get_user_model()
            if not User.objects.filter(
                                username=DJANGO_SUPERUSER_USERNAME).exists():
                user = User(
                    username=DJANGO_SUPERUSER_USERNAME,
                    email=DJANGO_SUPERUSER_EMAIL
                )
                user.set_password(DJANGO_SUPERUSER_PASSWORD)
                user.is_superuser = True
                user.is_staff = True
                user.is_admin = True
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    'Successfully created new superuser'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'Superuser already exists'))

        except Exception as e:
            raise CommandError(e)
