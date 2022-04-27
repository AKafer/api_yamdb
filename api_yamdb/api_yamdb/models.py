from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    composition = models.ForeignKey(Titles, on_delete=models.CASCADE)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    rating = models.FloatField(default=1)