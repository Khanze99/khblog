# Generated by Django 2.0.13 on 2019-11-01 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20191009_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
