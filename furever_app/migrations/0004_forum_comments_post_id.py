# Generated by Django 5.0.4 on 2024-11-19 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furever_app', '0003_forum_posts_pet_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum_comments',
            name='post_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
