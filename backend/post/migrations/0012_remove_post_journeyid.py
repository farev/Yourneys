# Generated by Django 4.2.3 on 2023-12-11 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_post_journeyid_alter_post_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='journeyID',
        ),
    ]