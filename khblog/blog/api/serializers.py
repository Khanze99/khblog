from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField,
                                        DateTimeField,
                                        ImageField)
from blog.models import Post


class PostCreateSerializers(ModelSerializer):
    image = ImageField(allow_null=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'image'
        )


class PostListSerializers(ModelSerializer):
    user = SerializerMethodField
    url = HyperlinkedIdentityField(
        view_name='detail_api',
        lookup_field='pk'
    )
    created_date = DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'id',
            'title',
            'created_date'
        )

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializers(ModelSerializer):
    created_date = DateTimeField(format="%d.%m.%Y %H:%M:%S")
    update_date = DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Post
        fields = (
            '__all__'
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