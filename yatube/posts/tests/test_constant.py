from django.urls import reverse

USERNAME_1 = 'TestUser1'
USERNAME_2 = 'TestUser2'
USERNAME_3 = 'TestUser3'
GROUP_SLUG_1 = 'test_slug_1'
GROUP_SLUG_2 = 'test_slug_2'
GROUP_TITLE_1 = 'Тестовая группа_1'
GROUP_TITLE_2 = 'Тестовая группа_2'
GROUP_DESCRIPTION = 'Описание группы'

INDEX_URL = reverse('posts:index')
POST_CREATE_URL = reverse('posts:post_create')
GROUP_LIST_URL = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG_1})
PROFILE_URL = reverse('posts:profile', kwargs={'username': USERNAME_1})
FOLLOW_INDEX_URL = reverse('posts:follow_index')

INDEX_TEMPLATE = 'posts/index.html'
POST_CREATE_TEMPLATE = 'posts/create_post.html'
POST_EDIT_TEMPLATE = 'posts/create_post.html'
GROUP_LIST_TEMPLATE = 'posts/group_list.html'
PROFILE_TEMPLATE = 'posts/profile.html'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
UNKNOWN_PAGE_TEMPLATE = 'core/404.html'
FOLLOW_INDEX_TEMPLATE = 'posts/follow.html'

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
