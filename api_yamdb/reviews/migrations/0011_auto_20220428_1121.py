# Generated by Django 2.2.16 on 2022-04-28 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_category_comment_genre_review_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='composition',
            new_name='title',
        ),
    ]