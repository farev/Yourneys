# Generated by Django 4.2.3 on 2024-02-06 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_conversation_journey_conversation_journey'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationmessage',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]