# Generated by Django 4.2.3 on 2024-02-11 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0007_journey_groupchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='journey',
            name='only_me',
            field=models.BooleanField(default=False),
        ),
    ]
