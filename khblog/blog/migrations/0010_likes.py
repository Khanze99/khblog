# Generated by Django 2.0.13 on 2019-05-13 17:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_auto_20190513_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField(default=0, verbose_name='likes')),
                ('userliked', models.ManyToManyField(related_name='user_like_this', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]