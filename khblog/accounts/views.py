from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ChangePassword
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        pass
    return render(request, "blog/form_login.html", {'form': form, 'title': title})


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        try:
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            send_mail(subject="Welcome {}! to blog".format(user), message=settings.EMAIL_MESSAGE,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[email],
                      auth_user=settings.EMAIL_HOST_USER,
                      auth_password=settings.EMAIL_HOST_PASSWORD)
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            return redirect('/')
        except IntegrityError:
            login(request, authenticate(username=form.save(commit=False), password=form.cleaned_data.get('password')))
            return redirect('/')
    context = {
        'form': form,
        'title': title,


    }
    return render(request, "blog/registration_form.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def profile(request):
    users = 0
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            email = u_form.cleaned_data.get("email")
            username = u_form.cleaned_data.get("username")
            id = request.user.id
            user_info = User.objects.get(id=id)
            if email != user_info.email:
                send_mail(subject="{}! Update your info".format(username), message='''You changed your information about you.
                Respectfully''',
                          from_email=settings.DEFAULT_FROM_EMAIL,
                          recipient_list=[email],
                          auth_user=settings.EMAIL_HOST_USER,
                          auth_password=settings.EMAIL_HOST_PASSWORD)
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('profile')
    else:
        users = User.objects.all().count()
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'users': users
    }
    return render(request, "registration/profile.html", context)


@login_required(login_url='/need_login/')
def profiles(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(author=id)
    context = {"user": user, "posts": posts}
    return render(request, "registration/profiles.html", context=context)


def need_login(request):
    return render(request, 'registration/need_login.html')


@login_required
def token_for_api(request, uid):
    user = User.objects.get(id=uid)
    token = Token.objects.get_or_create(user=user)[0]
    return render(request, 'registration/token.html', {'token': token})
