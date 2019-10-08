from . import views
from django.urls import path


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<pk>/publish', views.post_publish, name='post_publish'),
    path('post/<pk>/remove', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/comment/reply/<int:cid>/<int:uid>/', views.reply_comment, name='reply'),
    path('post/<int:pk>/<int:id>/remove_comment', views.remove_comment, name='remove_comment'),
    path('post/<int:pk>/<int:id>/edit_comment', views.edit_comment, name='edit_comment'),
    path('post/my_posts/', views.my_posts, name='my_posts'),
    path('post/<int:pk>/<int:id>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/<int:id>/dislike', views.post_dislike, name='post_dislike'),
    path('post/liked_posts/<int:id>', views.get_liked_post, name='liked_posts'),
    path('post/user_posts/<int:id>', views.get_user_posts, name='user_posts'),
    path('khamidov/', views.about_admin, name='khamidov')

]
