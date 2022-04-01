from django.test import TestCase

from posts.models import Group, Post, User
from posts.tests import test_constant as const


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_1)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=const.GROUP_SLUG_1,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        expected_post = post.text
        expected_group = group.title
        self.assertEqual(expected_post, str(post))
        self.assertEqual(expected_group, str(group))

    def test_help_texts(self):
        """Проверяем, что help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_verbose_names(self):
        """Проверяем, что verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_post_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество',
        }
        for value, expected in field_post_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)
        group = PostModelTest.group
        field_group_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for value, expected in field_group_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)
