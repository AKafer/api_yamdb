import pandas as pd

from django.core.management.base import BaseCommand

from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_data = pd.read_csv(
            'C:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\users.csv',
            sep=','
        )
        users = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
            )
            for i, row in tmp_data.iterrows()
        ]
        User.objects.bulk_create(users)
        print('Данные записаны в БД')
