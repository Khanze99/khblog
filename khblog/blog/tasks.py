from __future__ import absolute_import, unicode_literals
import logging

from celery import shared_task


from .models import Post
from .post_vk import API

logger = logging.getLogger('CELERY')


@shared_task
def send_post(id):
    obj = Post.objects.get(id=id)
    data = {'message': '{} \n {}'.format(obj.title, obj.text), 'path_images': []}
    if len(obj.images.all()) >= 1:
        for image in obj.images.all():
            data['path_images'].append(image.image.url)
        post = API(path_images=data['path_images'],
                   message=data['message'])
        return post.send()
    post = API(message=data['message'])
    return post.send()
