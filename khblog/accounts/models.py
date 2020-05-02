from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


from PIL import Image
from uuid import uuid4
import re


def upload_profile(instance, filename):
    pattern = r'.*\.(png|jpg|gif)'
    filename = filename.lower()
    formats = re.findall(pattern, filename)
    return '{}/{}.{}'.format(instance.user.id, uuid4().hex, formats[0])


def upload_projects_image(instance, filename):
    pattern = r'.*\.(png|jpg|gif)'
    filename = filename.lower()
    formats = re.findall(pattern, filename)
    return f'projects/{uuid4()}.{formats[0]}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='default-medium.png', upload_to=upload_profile)
    city = models.CharField(default='-', max_length=32)
    doing = models.TextField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    github_link = models.CharField(blank=True, null=True, max_length=100)
    github_username = models.CharField(blank=True, null=True, max_length=100)
    vk_link = models.CharField(blank=True, null=True, max_length=100)
    inst_username = models.CharField(blank=True, null=True, max_length=100)
    linkedin_link = models.CharField(blank=True, null=True, max_length=100)
    facebook_link = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f'Profile {self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.photo.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=510, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_projects_image)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ProjectImage, self).save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

