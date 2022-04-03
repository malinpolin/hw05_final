from django.test import TestCase

from posts.models import Comment, Follow, Group, Post, User
from posts.tests import test_constant as const


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=const.USERNAME_1)
        cls.user = User.objects.create_user(username=const.USERNAME_2)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=const.GROUP_SLUG_1,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.comment = Comment.objects.create(
            text='Текст комментария',
            post=cls.post,
            author=cls.user,
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        expected_post = self.post.text[:15]
        expected_group = self.group.title
        expected_comment = (
            f'{self.comment.text[:15]} '
            f'{self.comment.pub_date:%d %b %H:%M}'
        )
        self.assertEqual(expected_post, str(self.post))
        self.assertEqual(expected_group, str(self.group))
        self.assertEqual(expected_comment, str(self.comment))

    def test_help_texts(self):
        """Проверяем, что help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).help_text, expected)

    def test_verbose_names(self):
        """Проверяем, что verbose_name в полях совпадает с ожидаемым."""
        field_post_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество',
        }
        for value, expected in field_post_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected)
        field_group_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for value, expected in field_group_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).verbose_name, expected)
        field_comment_verboses = {
            'text': 'Текст комментария',
            'post': 'Пост',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
        }
        for value, expected in field_comment_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.comment._meta.get_field(value).verbose_name, expected)
        field_follow_verboses = {
            'user': 'Пользователь',
            'author': 'Автор',
        }
        for value, expected in field_follow_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.follow._meta.get_field(value).verbose_name, expected)
