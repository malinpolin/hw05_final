import shutil
import tempfile
from xml.etree.ElementTree import Comment

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms

from posts.models import Follow, Post, Group, Comment, User
from posts.tests import test_constant as const

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


def create_test_base(self, posts_count):
    """Создание тестовой базы."""
    posts_list = []
    for i in range(1, (posts_count // 2) + 1):
        if i % 3 == 0:
            posts_list.append(
                Post(
                    author=self.user_1,
                    text='Тестовый пост без группы'
                )
            )
            posts_list.append(
                Post(
                    author=self.user_2,
                    text='Тестовый пост без группы'
                )
            )
        elif i % 2 == 0:
            posts_list.append(
                Post(
                    author=self.user_1,
                    group=self.group_two,
                    text='Тестовый пост группы 2'
                )
            )
            posts_list.append(
                Post(
                    author=self.user_2,
                    group=self.group_two,
                    text='Тестовый пост группы 2'
                )
            )
        else:
            posts_list.append(
                Post(
                    author=self.user_1,
                    group=self.group_one,
                    text='Тестовый пост группы 1'
                )
            )
            posts_list.append(
                Post(
                    author=self.user_2,
                    group=self.group_one,
                    text='Тестовый пост группы 1'
                )
            )
    Post.objects.bulk_create(posts_list)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username=const.USERNAME_1)
        cls.user_2 = User.objects.create_user(username=const.USERNAME_2)
        cls.group_one = Group.objects.create(
            title=const.GROUP_TITLE_1,
            slug=const.GROUP_SLUG_1,
            description=const.GROUP_DESCRIPTION,
        )
        cls.group_two = Group.objects.create(
            title=const.GROUP_TITLE_2,
            slug=const.GROUP_SLUG_2,
            description=const.GROUP_DESCRIPTION,
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.SMALL_GIF,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user_1,
            group=cls.group_one,
            image=cls.uploaded,
            text='Последний пост с картинкой',
        )
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail',
            kwargs={'post_id': cls.post.id}
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit',
            kwargs={'post_id': cls.post.id}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_1)

    def check_context_for_list_pages(self, context, expected):
        """Проверка контекста для страниц index, group_list и profile"""
        first_object = context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_id_0 = first_object.id
        self.assertEqual(post_text_0, expected.text)
        self.assertEqual(post_author_0.id, expected.author.id)
        self.assertEqual(post_id_0, expected.id)
        if first_object.group:
            post_group_0 = first_object.group
            self.assertEqual(post_group_0.slug, expected.group.slug)
            self.assertEqual(post_group_0.id, expected.group.id)
            self.assertEqual(
                post_group_0.description,
                expected.group.description
            )
        if first_object.image:
            post_image_0 = first_object.image
            self.assertEqual(post_image_0, expected.image)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            const.INDEX_URL: const.INDEX_TEMPLATE,
            const.POST_CREATE_URL: const.POST_CREATE_TEMPLATE,
            const.GROUP_LIST_URL: const.GROUP_LIST_TEMPLATE,
            const.PROFILE_URL: const.PROFILE_TEMPLATE,
            self.POST_EDIT_URL: const.POST_EDIT_TEMPLATE,
            self.POST_DETAIL_URL: const.POST_DETAIL_TEMPLATE,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.INDEX_URL)
        expected_first_object = Post.objects.latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('title'),
            'Последние обновления на сайте'
        )

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.GROUP_LIST_URL)
        expected_first_object = Post.objects.filter(
            group=self.group_one
        ).latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('group').id,
            expected_first_object.group.id
        )

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_DETAIL_URL)
        self.assertEqual(
            response.context.get('post').author.id,
            self.post.author.id
        )
        self.assertEqual(
            response.context.get('post').text,
            self.post.text
        )
        self.assertEqual(
            response.context.get('title'),
            'Пост ' + self.post.text[:30]
        )
        self.assertEqual(
            response.context.get('post').image,
            'posts/small.gif'
        )

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.PROFILE_URL)
        expected_first_object = Post.objects.filter(
            author=self.user_1
        ).latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('title'),
            'Профайл пользователя ' + self.user_1.username
        )

    def test_create_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.POST_CREATE_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context.get('title'), 'Новый пост')

    def test_edit_show_correct_context(self):
        """Шаблон edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_EDIT_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(
            response.context.get('post').id,
            self.post.id
        )
        self.assertEqual(response.context.get('title'), 'Редактировать пост')
        self.assertTrue(response.context.get('is_edit'))

    def test_new_post(self):
        """Проверка отображения нового поста
        на страницах index, group_list, profile.
        Пост не попадает в другие группы и профайлы.
        """
        new_post = Post.objects.create(
            author=self.user_1,
            text='Новый пост в группе 2',
            group=self.group_two,
        )
        reverse_names_correct_pages = (
            const.INDEX_URL,
            reverse(
                'posts:group_list',
                kwargs={'slug': new_post.group.slug},
            ),
            const.PROFILE_URL,
        )
        for reverse_name in reverse_names_correct_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertIn(new_post, response.context['page_obj'])
        reverse_names_incorrect_pages = (
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_one.slug},
            ),
            reverse(
                'posts:profile',
                kwargs={'username': self.user_2.username},
            )
        )
        for reverse_name in reverse_names_incorrect_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertNotIn(new_post, response.context['page_obj'])

    def test_new_comment(self):
        """Авторизованный пользователь может добавить комментарий"""
        comment_count = Comment.objects.count()
        new_comment = Comment.objects.create(
            text='Новый комментарий',
            author=self.user_2,
            post=self.post,
        )
        response = self.authorized_client.get(self.POST_DETAIL_URL)
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertIn(new_comment, response.context['comments'])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username=const.USERNAME_1)
        cls.user_2 = User.objects.create_user(username=const.USERNAME_2)
        cls.group_one = Group.objects.create(
            title=const.GROUP_TITLE_1,
            slug=const.GROUP_SLUG_1,
            description=const.GROUP_DESCRIPTION,
        )
        cls.group_two = Group.objects.create(
            title=const.GROUP_TITLE_2,
            slug=const.GROUP_SLUG_2,
            description=const.GROUP_DESCRIPTION,
        )
        posts_count = 36
        create_test_base(cls, posts_count)

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_1)

    def check_pages_contains_correct_count_records(
        self,
        url,
        expected_count,
        url_kwargs={}
    ):
        """На каждой странице переданного URL требуемое кол-во постов"""
        paginator_count = settings.PAGINATOR_COUNT
        page_ten_count = expected_count // paginator_count
        page_count = (
            expected_count // paginator_count + 1
            if expected_count % paginator_count > 0
            else expected_count // paginator_count
        )
        while page_ten_count > 0:
            response = self.authorized_client.get(
                reverse(url, kwargs=url_kwargs) + f'?page={page_ten_count}'
            )
            self.assertEqual(
                len(response.context['page_obj']),
                paginator_count,
            )
            page_ten_count -= 1
        else:
            if page_count > page_ten_count:
                response = self.authorized_client.get(
                    reverse(url, kwargs=url_kwargs) + f'?page={page_count}'
                )
                self.assertEqual(
                    len(response.context['page_obj']),
                    expected_count % paginator_count,
                )

    def test_lists_pages_contains_correct_count_records(self):
        """На страницы index, group_list и profile передаётся
        ожидаемое количество объектов
        """
        url_kwargs = (
            (
                'posts:profile',
                {'username': self.user_1.username},
                Post.objects.filter(author=self.user_1).count()
            ),
            (
                'posts:group_list',
                {'slug': self.group_one.slug},
                Post.objects.filter(group=self.group_one).count()
            ),
            (
                'posts:index',
                {},
                Post.objects.count()
            ),
        )
        for url, kwargs, expected_count in url_kwargs:
            self.check_pages_contains_correct_count_records(
                url,
                expected_count,
                kwargs
            )


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_1)
        cls.post = Post.objects.create(
            author=cls.user,
            text='Новый пост'
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index_page(self):
        """Проверка кеширования главной страницы"""
        first_click = self.authorized_client.get(const.INDEX_URL)
        self.post.text = 'Отредактированный пост'
        self.post.save()
        second_click = self.authorized_client.get(const.INDEX_URL)
        self.assertEqual(first_click.content, second_click.content)
        cache.clear()
        third_click = self.authorized_client.get(const.INDEX_URL)
        self.assertNotEqual(first_click.content, third_click.content)


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_1)
        cls.follower = User.objects.create_user(username=const.USERNAME_2)
        cls.author = User.objects.create_user(username=const.USERNAME_3)
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост'
        )
        cls.FOLLOW_URL = reverse(
            'posts:profile_follow',
            kwargs={'username': cls.author.username}
        )
        cls.UNFOLLOW_URL = reverse(
            'posts:profile_unfollow',
            kwargs={'username': cls.author.username}
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        # Создаем авторизованный клиент - подписчика
        self.authorized_client_follower = Client()
        self.authorized_client_follower.force_login(self.follower)

    def test_follow(self):
        """Авторизованный пользователь может подписаться"""
        follow_count = Follow.objects.count()
        self.authorized_client_follower.get(self.FOLLOW_URL)
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.follower,
                author=self.author
            ).exists()
        )

    def test_unfollow(self):
        """Авторизованный пользователь может отписаться"""
        follow_count = Follow.objects.count()
        self.authorized_client_follower.get(self.FOLLOW_URL)
        self.authorized_client_follower.get(self.UNFOLLOW_URL)
        self.assertEqual(Follow.objects.count(), follow_count)
        self.assertFalse(
            Follow.objects.filter(
                user=self.follower,
                author=self.author
            ).exists()
        )

    def test_new_post_in_followers_feed(self):
        new_post = Post.objects.create(
            author=self.author,
            text='Новый пост'
        )
        self.authorized_client_follower.get(self.FOLLOW_URL)
        response = self.authorized_client_follower.get(const.FOLLOW_INDEX_URL)
        self.assertIn(new_post, response.context['page_obj'])
        response = self.authorized_client.get(const.FOLLOW_INDEX_URL)
        self.assertNotIn(new_post, response.context['page_obj'])
