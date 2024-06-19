from datetime import datetime

from django.test import TestCase

from content.models import Content
from users.models import User
from users.services import create_product, create_price, create_session


class ContentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            phone='+71111111111',
            first_name='Marta',
            last_name='Koshkina',
            email='marta.koshkina@gmail.com',
        )
        self.content = Content.objects.create(
            user=self.user,
            title='Title',
            text='Content',
            image='image.jpg',
        )

    def test_content_create_view(self):
        response = self.client.post('/create/')
        self.assertEqual(response.status_code, 200)
        new_content = Content.objects.create(
            title='Test',
            text='Testovich',
            image='image.jpg',
        )
        self.assertEqual(new_content.title, 'Test')
        self.assertEqual(new_content.user, None)

    def test_contentpersonal_list_view(self):
        response = self.client.get('/personal_list/')
        self.assertEqual(response.status_code, 302)

    def test_contentmanager_list_view(self):
        response = self.client.get('/manager_list/')
        self.assertEqual(response.status_code, 302)

    def test_statistics_view(self):
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 302)

    def test_likes(self):
        response = self.client.get(f'/likes/{self.content.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_content_list_view(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Content.objects.count(), 1)

    def test_user_update_view(self):
        response = self.client.patch(f'/update/{self.content.pk}/')
        self.assertEqual(response.status_code, 302)

        self.content.title = 'Test2'
        self.content.text = 'Testovich2'
        self.content.save()
        self.assertEqual(self.content.title, 'Test2')
        self.assertNotEqual(self.content.text, 'Testovich')

    def test_content_detail_view(self):
        response = self.client.get(f'/detail/{self.content.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.content.title, 'Title')
        self.assertEqual(self.content.text, 'Content')
        self.assertEqual(self.content.image, 'image.jpg')

    def test_user_delete_view(self):
        response = self.client.delete(f'/delete/{self.content.pk}/')
        self.assertEqual(response.status_code, 302)
        self.content.delete()
        self.assertEqual(Content.objects.count(), 0)

    def test_subscription(self):
        data = datetime.now().date()
        prod = create_product(self.content.pk, data)
        self.assertEqual(type(prod), str)
        price = create_price(prod)
        session, payment_url = create_session(price)
        self.assertEqual(type(session), str)
        self.assertEqual(type(payment_url), str)
