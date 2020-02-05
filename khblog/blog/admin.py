from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Post, Comment


class CommentsInline(admin.TabularInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_date', 'parent')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'text', 'image', 'get_liked_by', 'likes',
                    'get_disliked_by', 'dislikes', 'created_date', 'update_date', 'view', 'custom_button')
    inlines = (CommentsInline, )

    def custom_button(self, obj):
        links = ['<a class="button" href="{url}"> Перейти</a>'.format(url='/post/{}/'.format(obj.id))]
        return mark_safe('&nbsp;'.join(links))
    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['data'] = 'data'
    #     return super().changelist_view(
    #         request, extra_context=extra_context,
    #     )
