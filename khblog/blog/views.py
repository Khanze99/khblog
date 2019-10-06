from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


def post_list(request):
    search_query = request.GET.get('Search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) |
                                    Q(text__icontains=search_query)).order_by('-created_date')
    else:
        posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    if request.user.is_authenticated:
        comments_root = Comment.objects.filter(author=request.user)
        posts = Post.objects.filter(author=request.user)
        user_item = User.objects.filter(liked_by=pk)
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter(parent__isnull=True)
        post.view += 1
        post.save()
        return render(request, 'blog/post_detail.html', {'post': post, 'posts': posts,
                                                         'comments': comments,
                                                         'comments_root': comments_root,
                                                         'user_item': user_item,
                                                         'list_liked_by': post.liked_by.all(),
                                                         'list_disliked_by': post.disliked_by.all()})
    else:
        post = get_object_or_404(Post, pk=pk)
        post.view += 1
        post.save()
        return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to.html', {'form': form})


@login_required
def remove_comment(request, pk, id):
    comment = get_object_or_404(Comment, author=request.user, id=id)
    comment.delete()
    return redirect('post_detail', pk=pk)


@login_required
def edit_comment(request, pk, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


def post_like(request, id, pk):
    if request.user.is_authenticated:
        post_item = Post.objects.get(pk=pk)
        user_item_likes = User.objects.filter(liked_by=pk)  # список тех кто лайкнул данный пост по id
        user_item_dislikes = User.objects.filter(disliked_by=pk)  # Список тех кто дизлайкнул пост по id
        current_user = request.user
        if (current_user not in user_item_likes) and (current_user not in user_item_dislikes):
            try:
                post_item.likes += 1
                post_item.liked_by.add(current_user)
                post_item.save()
                return redirect('post_detail', pk=pk)
            except ObjectDoesNotExist:
                return redirect('post_detail', pk=pk)
        elif (current_user not in user_item_likes) and (current_user in user_item_dislikes):
            post_item.dislikes -= 1
            post_item.disliked_by.remove(current_user)
            post_item.likes += 1
            post_item.liked_by.add(current_user)
            post_item.save()
            return redirect('post_detail', pk=pk)
        elif current_user in user_item_likes:
            post_item.likes -= 1
            post_item.liked_by.remove(current_user)
            post_item.save()
            return redirect('post_detail', pk=pk)
        else:
            return redirect('post_detail', pk=pk)
    else:
        return redirect('post_detail', pk=pk)


def post_dislike(request, pk, id):
    if request.user.is_authenticated:
        user_item_disliked = User.objects.filter(disliked_by=pk)
        user_item_liked = User.objects.filter(liked_by=pk)
        post = Post.objects.get(pk=pk)
        user = request.user
        if (user not in user_item_disliked) and (user not in user_item_liked):
            post.dislikes += 1
            post.disliked_by.add(user)
            post.save()
            return redirect('post_detail', pk=pk)
        elif user in user_item_disliked:
            post.dislikes -= 1
            post.disliked_by.remove(user)
            post.save()
            return redirect('post_detail', pk=pk)
        elif (user in user_item_liked) and (user not in user_item_disliked):
            post.likes -= 1
            post.liked_by.remove(user)
            post.dislikes += 1
            post.disliked_by.add(user)
            post.save()
            return redirect('post_detail', pk=pk)
        else:
            return redirect('post_detail', pk=pk)
    else:
        return redirect('post_detail', pk=pk)


def get_liked_post(request, id):
    posts = Post.objects.all().order_by('-created_date')
    liked_posts = []
    user = User.objects.get(id=id)
    for post in posts:
        if user in post.liked_by.all():
            liked_posts.append(post)
    return render(request, 'blog/liked_posts.html', {'liked_posts': liked_posts})


def get_user_posts(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/user_posts.html', context={'posts': posts})


def reply_comment(request, uid, pk, cid):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=uid)
            post = Post.objects.get(pk=pk)
            reply_comment_to_user = Comment.objects.get(id=cid)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.parent = reply_comment_to_user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to.html', {'form': form})


def view_404(request):
    """
    :param request:
    :return:
    """
    return render(request, 'blog/404.html')


def view_500(request):
    """
    :param request:
    :return:
    """
    return render(request, 'blog/500.html')
