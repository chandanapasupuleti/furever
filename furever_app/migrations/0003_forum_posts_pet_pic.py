# Generated by Django 5.0.4 on 2024-11-10 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furever_app', '0002_forum_comments_forum_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum_posts',
            name='pet_pic',
            field=models.BinaryField(default=None),
        ),
    ]
