# Generated by Django 4.2.3 on 2023-10-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_post_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='label',
            field=models.CharField(choices=[('Start', 'Start'), ('Update', 'Update'), ('Milestone', 'Milestone'), ('End', 'End')], default='Start', max_length=10),
        ),
    ]
