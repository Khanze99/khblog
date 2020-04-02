from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        IsAdminUser)
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication

from blog.models import Post, Comment
from .serializers import (PostListSerializers,
                          PostDetailSerializers,
                          PostCreateSerializers,
                          PostUpdateSerializer,
                          CommentSerializer)
from blog.tasks import send_post


class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListApiView(ListAPIView):
    serializer_class = PostListSerializers
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset_list = Post.objects.all()
        query = self.request.GET.get('Search', None)
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query)
            )
        return queryset_list


class PostUPDATEApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticated]


class PostDeleteApiView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({'{}'.format(pk): 'deleted'})


class PostDetailAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializers
    permission_classes = [IsAuthenticated]


class CommentListApi(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.kwargs['pk'])
        return queryset


class PostVkApiView(APIView):

    def get(self, request):
        post_id = None
        response = {'Error': 'No related params'}
        status = 400
        if request.GET:
            if 'post_id' in request.GET:
                post_id = request.GET.get('post_id')

        if request.user.is_staff:

            if post_id is not None:
                send_post.delay(post_id)
                response = {'Message': 'Params have been submitted for processing'}
                status = 200

        return Response(response, status=status)
