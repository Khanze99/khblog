from django.urls import path
from .views import (PostListApiView,
                    PostDetailAPIView,
                    PostUPDATEApiView,
                    PostDeleteApiView,
                    PostCreateApiView,
                    CommentListApi,
                    PostVkApiView,
                    LikePostView,
                    DisLikePostView)


urlpatterns = [
    path('api/posts/', PostListApiView.as_view(), name='list'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='detail_api'),
    path('api/posts/<int:pk>/update/', PostUPDATEApiView.as_view(), name='update'),
    path('api/posts/<int:pk>/delete/', PostDeleteApiView.as_view(), name='delete'),
    path('api/posts/create/', PostCreateApiView.as_view(), name='create'),
    path('api/posts/<int:pk>/comments/', CommentListApi.as_view(), name='comments'),
    path('api/postToVk', PostVkApiView.as_view(), name='post_to_vk'),
    path('api/post/like/', LikePostView.as_view(), name='like'),
    path('api/post/dislike/', DisLikePostView.as_view(), name='dislike')
]