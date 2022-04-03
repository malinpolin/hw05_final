import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Comment, User
from posts.tests import test_constant as const

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_1)
        cls.post = Post.objects.create(
            text='Старый пост',
            author=cls.user
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.SMALL_GIF,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Новый пост',
            'image': uploaded
        }
        response = self.authorized_client.post(
            const.POST_CREATE_URL,
            data=form_data,
            follow=True,
        )
        new_post = Post.objects.latest('pub_date')
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': new_post.author.username},
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                id=new_post.id,
                author=new_post.author,
                image='posts/small.gif',
            ).exists()
        )

    def test_post_edit(self):
        """Валидная форма редактирует запись в Post."""
        post_count = Post.objects.count()
        new_uploaded = SimpleUploadedFile(
            name='new_small.gif',
            content=const.SMALL_GIF,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Отредактированный пост',
            'image': new_uploaded,
        }
        last_post = Post.objects.last()
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': last_post.id}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': last_post.id},
            )
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                id=last_post.id,
                author=last_post.author,
                image='posts/new_small.gif'
            ).exists()
        )

    def test_post_text_help_text(self):
        text_help_text = self.form.fields['text'].help_text
        self.assertEqual(text_help_text, 'Текст нового поста')

    def test_guest_cant_add_comment(self):
        """Неавторизованный пользователь не может оставить комментарий"""
        form_data = {
            'text': 'Комментарий от гостя',
        }
        self.guest_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.id}
            ),
            data=form_data,
            follow=True,
        )
        self.assertFalse(
            Comment.objects.filter(
                text=form_data['text']
            ).exists()
        )
