# Generated by Django 2.2.16 on 2022-04-28 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_auto_20220428_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
