from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render

from .models import Post, Comment, Image
from accounts.forms import ProfilesForm


class CommentsInline(admin.TabularInline):
    model = Comment


class ImagesInline(admin.TabularInline):
    model = Image


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_date', 'parent')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    change_list_template = 'admin/blog/change_list.html'
    list_display = ('id', 'author', 'title', 'text', 'get_liked_by', 'likes',
                    'get_disliked_by', 'dislikes', 'created_date', 'update_date', 'custom_button')
    inlines = (CommentsInline, ImagesInline)

    def get_urls(self):
        # Расширяем юрлы для админки через вложение модели
        urls = super().get_urls()
        custom_urls = [
            path('permissions/<int:pk>/', self.get_permissions, name='test')
        ]
        return custom_urls + urls

    def custom_button(self, obj):
        # Создаем кнопку для каждого объекта на странице html
        link = f'<a class="button" href="permissions/{obj.id}/">TEST</a>'
        return format_html(link)
    custom_button.short_description = 'TEST'

    def get_permissions(self, request, pk):
        # Тут будет происходить вся логика к которому мы будет оправлять запросы с формы
        obj = Post.objects.get(pk=pk)
        form = ProfilesForm()
        return render(request, 'admin/blog/test.html', {'form': form, 'obj': obj})

