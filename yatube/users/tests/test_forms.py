from django.test import Client, TestCase
from django.urls import reverse

from users.forms import CreationForm
from posts.models import User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CreationForm()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_user_signup(self):
        """Валидная форма создает запись в Post."""
        user_count = User.objects.count()
        form_data = {
            'first_name': 'Polina',
            'last_name': 'Doroshenko',
            'username': 'malinpolin',
            'email': 'malinpolin@gmail.com',
            'password1': 'testpass1',
            'password2': 'testpass1',

        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:index'),
        )
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                username=form_data['username'],
                email=form_data['email'],
            ).exists()
        )
