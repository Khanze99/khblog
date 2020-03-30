from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        DateTimeField,
                                        ImageField)
from blog.models import Post, Comment


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
    comments = HyperlinkedIdentityField(view_name='comments', lookup_field='pk')
    url = HyperlinkedIdentityField(
        view_name='detail_api',
        lookup_field='pk'
    )
    created_date = DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'id',
            'title',
            'created_date',
            'comments'
        )

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializers(ModelSerializer):
    created_date = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = (
            '__all__'
        )


class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            '__all__'
        )
