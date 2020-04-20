from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from .models import Post, Comment, Image, IPView
from .forms import PostForm, CommentForm, ImageForm
from .helpers import get_client_ip


def post_list(request):
    search_query = request.GET.get('Search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) |
                                    Q(text__icontains=search_query))
    else:
        posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    ip = get_client_ip(request)
    post = get_object_or_404(Post, pk=pk)
    flag = IPView.objects.filter(ip=ip, post=post).exists()
    if flag is False:
        IPView(ip=ip, user=request.user, post=post).save()
    views = IPView.objects.filter(post=post).count()
    if request.user.is_authenticated:
        comments_root = Comment.objects.filter(author=request.user)
        posts = Post.objects.filter(author=request.user)
        user_item = User.objects.filter(liked_by=pk)
        comments = post.comments.filter(parent__isnull=True)
        return render(request, 'blog/post_detail.html', {'post': post, 'posts': posts,
                                                         'views': views,
                                                         'images': post.images.all(),
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for file in request.FILES.getlist('image'):
                Image(post=post, image=file).save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        image_form = ImageForm()
        return render(request, 'blog/post_new.html', {'form': form, 'image_form': image_form})


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
        image_formset = modelformset_factory(Image)
    return render(request, 'blog/edit_comment.html', {'form': form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def get_liked_post(request, id):
    posts = Post.objects.all().order_by('-created_date')
    liked_posts = []
    user = User.objects.get(id=id)
    for post in posts:
        if user in post.liked_by.all():
            liked_posts.append(post)
    return render(request, 'blog/liked_posts.html', {'liked_posts': liked_posts})


@login_required
def get_user_posts(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/user_posts.html', context={'posts': posts})


@login_required
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


def view_404(request, *args, **kwargs):
    response = render_to_response('blog/404.html', context={'user': request.user, 'request': request})
    response.status_code = 404
    return response


def view_500(request, *args, **kwargs):
    response = render_to_response('blog/500.html', context={'user': request.user, 'request': request})
    response.status_code = 500
    return response


def view_403(request, *args, **kwargs):
    response = render_to_response('blog/403.html', context={'user': request.user, 'request': request})
    response.status_code = 403
    return response
