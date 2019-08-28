from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from blog.models import Post


class PostCreateSerializers(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'published_date'
        )


class PostListSerializers(ModelSerializer):
    user = SerializerMethodField
    url = HyperlinkedIdentityField(
        view_name='detail_api',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'id',
            'title',
            'text',
            'published_date'
        )

    def get_user(self, obj):
        return str(obj.user.username)



class PostDetailSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='detail_api',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'author',
            'title',
            'text',
            'published_date'
        )



"""
data = {
    'title': 'test a',
    'text' : 'test a)))',
    'created_date': '2019-20-6',
    
}


from blog.models import Post
from blog.api.serializers import PostDetailSerializers

obj = Post.objects.get(id=40)
obj_data = PostDetailSerializers(obj)

new_data = PostDetailSerializers(obj, data)
if new_data.is_valid():
    new_data.save()
else:
    print(new_data.errors)

"""