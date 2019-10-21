from .models import Post
from .post_vk import API


def send_post(id):
    obj = Post.objects.get(id=id)
    data = {'message': '{} {}'.format(obj.title, obj.text)}
    if obj.image:
        data.update({'path_image': obj.image.url})
        post = API(path_image=data['path_image'],
                   message=data['message'])
        post.send()
    post = API(message=data['message'])

