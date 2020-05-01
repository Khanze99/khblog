from django.contrib import admin
from .models import Profile, Project, ProjectImage


class ProjectsTabularInlines(admin.TabularInline):
    model = Project


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProjectsTabularInlines, ]
    list_display = ('id', 'user', 'photo', 'city', 'doing', 'about_me',
                    'github_link',  'github_username', 'vk_link', 'inst_username', 'linkedin_link',
                    'facebook_link')


class ProjectsImagesInlines(admin.TabularInline):
    model = ProjectImage


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'description')
    inlines = [ProjectsImagesInlines, ]

