from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone='+79000000000',
            email='BlueberryRainbows@yandex.ru',
            first_name='Admin',
            last_name='Adminow',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Ad.Min00')
        user.save()
