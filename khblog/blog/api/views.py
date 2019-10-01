from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)
from blog.models import Post
from .serializers import PostListSerializers, PostDetailSerializers, PostCreateSerializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
                                        AllowAny,
                                        IsAuthenticated,
                                        IsAdminUser,
                                        IsAuthenticatedOrReadOnly,)
from .permission import IsOwnerOrReadOnly
from django.db.models import Q


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
    serializer_class = PostListSerializers
    permission_classes = [IsAuthenticated]


class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializers
    permission_classes = [IsAuthenticated]


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializers
    permission_classes = [IsAuthenticated]
