# Generated by Django 4.2.3 on 2023-12-14 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_alter_post_journeyid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='journeyID',
            field=models.TextField(blank=True, null=True),
        ),
    ]
