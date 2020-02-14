from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render

from .models import Post, Comment
from accounts.forms import ProfilesForm


class CommentsInline(admin.TabularInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_date', 'parent')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    change_list_template = 'admin/blog/change_list.html'
    list_display = ('id', 'author', 'title', 'text', 'image', 'get_liked_by', 'likes',
                    'get_disliked_by', 'dislikes', 'created_date', 'update_date', 'view', 'custom_button')
    inlines = (CommentsInline, )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('permissions/<int:pk>/', self.get_permissions)
        ]
        return custom_urls + urls

    def custom_button(self, obj):
        link = f'<a class="button" href="permissions/{obj.id}/">TEST</a>'
        return format_html(link)
    custom_button.short_description = 'TEST'

    def get_permissions(self, request, pk):
        print(pk)
        form = ProfilesForm()
        return render(request, 'accounts/fo_form.html', {'form': form})

