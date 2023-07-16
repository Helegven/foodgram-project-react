from django import forms

from .models import Recipe


class PostForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)
#         labels = {
#             'text': 'Текст',
#         }
#         help_texts = {
#             'text': 'Текст нового комментария',
#         }