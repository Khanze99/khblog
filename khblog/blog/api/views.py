from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Post, Comment
from .serializers import (PostListSerializers,
                          PostDetailSerializers,
                          PostCreateSerializers,
                          PostUpdateSerializer,
                          CommentSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
                                        AllowAny,
                                        IsAuthenticated,
                                        IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token



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
