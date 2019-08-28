from django.urls import path
from .views import PostListApiView, PostDetailAPIView, PostUPDATEApiView, PostDeleteApiView, PostCreateApiView


urlpatterns = [
    path('api/posts/', PostListApiView.as_view(), name='list'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='detail_api'),
    path('api/posts/<int:pk>/update/', PostUPDATEApiView.as_view(), name='update'),
    path('api/posts/<int:pk>/delete/', PostDeleteApiView.as_view(), name='delete'),
    path('api/posts/create/', PostCreateApiView.as_view(), name='create')
]