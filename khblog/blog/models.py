from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def upload_location(instance, filename):
    return "post/{}".format(filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True)
    text = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_by")
    likes = models.IntegerField(default=0, verbose_name="likes")
    disliked_by = models.ManyToManyField(User, related_name="disliked_by")
    dislikes = models.IntegerField(default=0, verbose_name="dislikes")
    created_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    view = models.IntegerField(default=0, verbose_name='views')

    def __str__(self):
        return self.title

    def get_liked_by(self):
        return ", ".join([user.username for user in self.liked_by.all()])

    def get_disliked_by(self):
        return ", ".join([user.username for user in self.disliked_by.all()])

    class Meta:
        ordering = ['-created_date']


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_date']

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return self.text

