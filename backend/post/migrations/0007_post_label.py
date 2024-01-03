# Generated by Django 4.2.3 on 2023-10-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_reported_by_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='label',
            field=models.CharField(choices=[('START', 'Start'), ('UPDATE', 'Update'), ('MS', 'Milestone'), ('END', 'End')], default='START', max_length=6),
        ),
    ]