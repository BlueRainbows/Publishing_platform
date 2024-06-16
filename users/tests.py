from datetime import datetime

from django.test import TestCase
from psycopg2 import DataError

from users.models import User, Subscription


class UserModelTest(TestCase):

    def setUp(self):
        self.object = User.objects.create(
            phone='+71111111111',
            first_name='Marta',
            last_name='Koshkina',
            email='marta.koshkina@gmail.com',
        )

    def test_user_create_view(self):
        new_user = User.objects.create(
            phone='+72222222222',
            first_name='Marta',
            last_name='Okroshkina',
            email='marta.okroshkina@gmail.com',
        )
        self.assertEqual(new_user.phone, '+72222222222')

    def test_user_update_view(self):
        self.object.phone = '+72222222222'
        self.object.email = 'marta.okroshkina@gmail.com'
        self.object.save()
        self.assertEqual(self.object.phone, '+72222222222')
        self.assertNotEqual(self.object.email, 'marta.koshkina@gmail.com')

    def test_user_delete_view(self):
        self.object.delete()
        self.assertEqual(User.objects.count(), 0)


class SubscriptionModelTest(TestCase):

    def test_subscription_create_view(self):
        datas = datetime.now().date()
        new_subscription = Subscription.objects.create(
            payment_data=datas,
        )
        self.assertEqual(new_subscription.payment_data, datas)
