# Generated by Django 2.2.16 on 2022-04-30 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0021_auto_20220430_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]