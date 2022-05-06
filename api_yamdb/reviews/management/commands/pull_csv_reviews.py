import pandas as pd

from django.core.management.base import BaseCommand

from reviews.models import Review, Title, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_data = pd.read_csv(
            'C:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\review.csv',
            sep=','
        )
        reviews = [
            Review(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )
            for i, row in tmp_data.iterrows()
        ]
        Review.objects.bulk_create(reviews)
        print('Данные записаны в БД')
