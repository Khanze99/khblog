from django import forms
from .models import Post, Comment, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')

    class Meta:
        model = Image
        fields = ('image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
