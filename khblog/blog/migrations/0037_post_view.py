# Generated by Django 2.0.13 on 2020-04-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_auto_20200420_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view',
            field=models.IntegerField(default=0, verbose_name='views'),
        ),
    ]