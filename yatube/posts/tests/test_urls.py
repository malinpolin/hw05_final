from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import Post, Group, User
from posts.tests import test_constant as const


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username=const.USERNAME_1)
        cls.user = User.objects.create_user(username=const.USERNAME_2)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE_1,
            slug=const.GROUP_SLUG_1,
            description=const.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовый пост',
        )

    def setUp(self):
        # Создаём неавторизованного клиента
        self.guest_client = Client()
        # Создаем авторизованного клиента - автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user_author)
        # Создаем авторизованного клиента - не автора поста
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_url_for_unauthorized_user(self):
        """Проверяем доступность страниц для анонимного пользователя"""
        url_names_codes = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user.username}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            '/unknown_page/': HTTPStatus.NOT_FOUND,
        }
        for url, code in url_names_codes.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, code)

    def test_create_url_for_authorized_user(self):
        """Доступность страниц для авторизованного пользователя (автора)"""
        urls = (
            '/create/',
            f'/posts/{self.post.id}/edit/',
            '/follow/'
        )
        for url in urls:
            response = self.authorized_client_author.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous(self):
        """Страницы create и follow перенаправляют анонимного пользователя"""
        url_names = (
            '/create/',
            '/follow/'
        )
        prefix = '/auth/login/?next='
        for url in url_names:
            response = self.guest_client.get(url, follow=True)
            self.assertRedirects(response, prefix + url)

    def test_edit_url_redirect_not_author(self):
        """Страница /posts/post.id/edit/ перенаправляет
        авторизованного пользователя - не автора.
        """
        url = f'/posts/{self.post.id}/edit/'
        response = self.authorized_client.get(url, follow=True)
        self.assertRedirects(response, f'/posts/{self.post.id}/')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': const.INDEX_TEMPLATE,
            f'/group/{self.group.slug}/': const.GROUP_LIST_TEMPLATE,
            f'/profile/{self.user.username}/': const.PROFILE_TEMPLATE,
            f'/posts/{self.post.id}/': const.POST_DETAIL_TEMPLATE,
            f'/posts/{self.post.id}/edit/': const.POST_EDIT_TEMPLATE,
            '/create/': const.POST_CREATE_TEMPLATE,
            '/unknown_page/': const.UNKNOWN_PAGE_TEMPLATE,
            '/follow/': const.FOLLOW_INDEX_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url)
                self.assertTemplateUsed(response, template)
