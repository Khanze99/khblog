# Generated by Django 2.0.13 on 2019-10-09 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_post_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='bio',
        ),
    ]
