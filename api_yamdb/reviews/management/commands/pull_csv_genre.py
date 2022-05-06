import pandas as pd

from django.core.management.base import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_data = pd.read_csv(
            'C:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\genre.csv',
            sep=','
        )
        genres = [
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for i, row in tmp_data.iterrows()
        ]
        Genre.objects.bulk_create(genres)
