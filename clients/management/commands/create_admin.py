from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='mutinda').exists():
            User.objects.create_superuser('mutinda', 'eminentwriters8@gmail.com', '123admin')
            self.stdout.write(self.style.SUCCESS('Superuser created: mutinda / 123admin'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
