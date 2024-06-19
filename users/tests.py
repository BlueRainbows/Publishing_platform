from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
import base64
from users.models import User, Subscription


class UserModelTest(TestCase):

    def setUp(self):
        self.object = User.objects.create(
            phone='+71111111111',
            first_name='Marta',
            last_name='Koshkina',
            email='marta.koshkina@gmail.com',
        )
        self.object.set_password('12345')
        self.object.save()

    def test_authorized(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
                                  base64.b64encode(b'phone:password').decode("ascii")
        }
        response = self.client.get('/', **headers)
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        response = self.client.post('/register/')
        self.assertEqual(response.status_code, 200)
        new_user = User.objects.create(
            phone='+72222222222',
            first_name='Marta',
            last_name='Okroshkina',
            email='marta.okroshkina@gmail.com',
            password='marta.okroshkina2'
        )
        new_user.set_password('12345')
        new_user.save()
        login_user = self.client.login(phone='+72222222222', password='12345')
        self.assertTrue(login_user)
        self.assertEqual(new_user.phone, '+72222222222')

        User.objects.create(
            phone='82222222222',
            first_name='Marta',
            last_name='Okroshkina',
            email='marta.okroshkina@gmail.com',
            password='marta.okroshkina2'
        )
        self.assertRaises(ValidationError)

    def test_user_detail_view(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.object.phone, '+71111111111')
        self.assertEqual(self.object.email, 'marta.koshkina@gmail.com')

    def test_user_update_view(self):
        response = self.client.post('/change_profile/')
        self.assertEqual(response.status_code, 302)
        self.object.phone = '+72222222222'
        self.object.email = 'marta.okroshkina@gmail.com'
        self.object.save()
        self.assertEqual(self.object.phone, '+72222222222')
        self.assertNotEqual(self.object.email, 'marta.koshkina@gmail.com')

    def test_user_delete_view(self):
        response = self.client.delete('/user_delete/')
        self.assertEqual(response.status_code, 302)
        self.object.delete()
        self.assertEqual(User.objects.count(), 0)


class SubscriptionModelTest(TestCase):

    def test_subscription_create_view(self):
        datas = datetime.now().date()
        new_subscription = Subscription.objects.create(
            payment_data=datas,
        )
        self.assertEqual(new_subscription.payment_data, datas)
