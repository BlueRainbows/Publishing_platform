
from django.test import TestCase

from content.models import Content
from users.models import User


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

    def test_user_create_view(self):
        new_content = Content.objects.create(
            title='Test',
            text='Testovich',
            image='image.jpg',
        )
        self.assertEqual(new_content.title, 'Test')
        self.assertEqual(new_content.user, None)

    def test_content_list_view(self):
        self.assertEqual(Content.objects.count(), 1)

    def test_user_update_view(self):
        self.content.title = 'Test2'
        self.content.text = 'Testovich2'
        self.content.save()
        self.assertEqual(self.content.title, 'Test2')
        self.assertNotEqual(self.content.text, 'Testovich')

    def test_content_detail_view(self):
        self.assertEqual(self.content.title, 'Title')
        self.assertEqual(self.content.text, 'Content')
        self.assertEqual(self.content.image, 'image.jpg')

    def test_user_delete_view(self):
        self.content.delete()
        self.assertEqual(Content.objects.count(), 0)
