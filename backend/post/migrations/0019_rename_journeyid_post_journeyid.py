# Generated by Django 4.2.3 on 2023-12-17 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0018_postattachment_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='journeyID',
            new_name='journeyid',
        ),
    ]
