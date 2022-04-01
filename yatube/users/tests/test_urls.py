from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import User

from users.tests import test_constants as const


class UserURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_url_for_unauthorized_user(self):
        """Проверяем доступность страниц для любого пользователя"""
        url_names = (
            '/auth/login/',
            '/auth/logout/',
            '/auth/signup/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
        )
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_url_for_authorized_user(self):
        """Проверяем доступность страниц /password_change/
        для авторизованного пользователя.
        """
        url_names = (
            '/auth/password_change/',
            '/auth/password_change/done/',
        )
        for url in url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_url_redirect_anonymous(self):
        """Страницы /password_change/ перенаправляют анонимного
        пользователя.
        """
        prefix = '/auth/login/?next='
        url_names = (
            '/auth/password_change/',
            '/auth/password_change/done/',
        )
        for url in url_names:
            response = self.guest_client.get(url, follow=True)
            redirect_address = prefix + url
            self.assertRedirects(response, redirect_address)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            const.SIGNUP_TEMPLATE: '/auth/signup/',
            const.LOGIN_TEMPLATE: '/auth/login/',
            const.PASSWORD_CHANGE_TEMPLATE: '/auth/password_change/',
            const.PASSWORD_CHANGE_DONE_TEMPLATE:
                '/auth/password_change/done/',
            const.PASSWORD_RESET_TEMPLATE: '/auth/password_reset/',
            const.PASSWORD_RESET_DONE_TEMPLATE: '/auth/password_reset/done/',
            const.PASSWORD_RESET_CONFIRM_TEMPLATE:
                '/auth/reset/<uidb64>/<token>/',
            const.PASSWORD_RESET_COMPLETE_TEMPLATE: '/auth/reset/done/',
            const.LOGOUT_TEMPLATE: '/auth/logout/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
