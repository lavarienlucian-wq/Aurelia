import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update a Django superuser from environment variables.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-if-missing',
            action='store_true',
            help='Do nothing when required superuser environment variables are missing.',
        )

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            if options['skip_if_missing']:
                self.stdout.write(
                    'Skipped superuser setup because username or password is missing.'
                )
                return
            raise CommandError(
                'Set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD.'
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        changed = created
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            changed = True
        if email and user.email != email:
            user.email = email
            changed = True

        user.set_password(password)
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} superuser "{username}".'))
