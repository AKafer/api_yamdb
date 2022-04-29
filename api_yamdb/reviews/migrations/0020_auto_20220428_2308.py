# Generated by Django 2.2.16 on 2022-04-28 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='reviews.Genre', verbose_name='Жанр(ы)'),
        ),
    ]
