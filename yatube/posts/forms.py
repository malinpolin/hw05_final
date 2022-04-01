from django import forms

from posts.models import Post, Group, Comment


class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        help_text='Группа, к которой будет относиться пост',
        label='Название группы',
    )

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {'text': 'Текст нового поста'}
        labels = {'text': 'Текст поста'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        help_texts = {'text': 'Текст нового комментария'}
        labels = {'text': 'Текст комментария'}
