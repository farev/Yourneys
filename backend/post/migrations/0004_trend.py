# Generated by Django 4.2.3 on 2023-08-28 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_comments_count_comment_post_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=255)),
                ('occurences', models.IntegerField()),
            ],
        ),
    ]
