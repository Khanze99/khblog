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


class LikePostView(APIView):
    def post(self, request):
        pk = request.POST.get('pk')
        post_item = Post.objects.get(pk=pk)
        user_item_likes = User.objects.filter(liked_by=pk)  # список тех кто лайкнул данный пост по id
        user_item_dislikes = User.objects.filter(disliked_by=pk)  # Список тех кто дизлайкнул пост по id
        current_user = request.user
        if (current_user not in user_item_likes) and (current_user not in user_item_dislikes):
            try:
                post_item.likes += 1
                post_item.liked_by.add(current_user)
                post_item.save()
            except ObjectDoesNotExist:
                return Response({'likes': post_item.likes, 'dislikes': post_item.dislikes, 'error': 'ObjectDoesNotExist'}, status=200)
        elif (current_user not in user_item_likes) and (current_user in user_item_dislikes):
            post_item.dislikes -= 1
            post_item.disliked_by.remove(current_user)
            post_item.likes += 1
            post_item.liked_by.add(current_user)
            post_item.save()
        elif current_user in user_item_likes:
            post_item.likes -= 1
            post_item.liked_by.remove(current_user)
            post_item.save()

        return Response({'likes': post_item.likes, 'dislikes': post_item.dislikes}, status=200)


class DisLikePostView(APIView):

    def post(self, request):
        pk = request.POST.get('pk')
        user_item_disliked = User.objects.filter(disliked_by=pk)
        user_item_liked = User.objects.filter(liked_by=pk)
        post = Post.objects.get(pk=pk)
        user = request.user
        if (user not in user_item_disliked) and (user not in user_item_liked):
            post.dislikes += 1
            post.disliked_by.add(user)
            post.save()
        elif user in user_item_disliked:
            post.dislikes -= 1
            post.disliked_by.remove(user)
            post.save()
        elif (user in user_item_liked) and (user not in user_item_disliked):
            post.likes -= 1
            post.liked_by.remove(user)
            post.dislikes += 1
            post.disliked_by.add(user)
            post.save()

        return Response({'likes': post.likes, 'dislikes': post.dislikes}, status=200)
