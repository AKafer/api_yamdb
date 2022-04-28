# Generated by Django 2.2.16 on 2022-04-28 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20220428_1241'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review_author',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]
