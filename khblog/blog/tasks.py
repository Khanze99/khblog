from __future__ import absolute_import, unicode_literals
import logging

from celery import shared_task


from .models import Post
from .post_vk import API

logger = logging.getLogger('CELERY')


@shared_task
def send_post(id):
    obj = Post.objects.get(id=id)
    data = {'message': '{} \n {}'.format(obj.title, obj.text)}
    if obj.image:
        data.update({'path_image': obj.image.url})
        post = API(path_image=data['path_image'],
                   message=data['message'])
        return post.send()
    post = API(message=data['message'])
    return post.send()
