from pickle import FALSE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(max_length=150, unique=True) # Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
    email = models.EmailField(max_length=254, unique=True)  # required, string <email> <= 254 characters
    first_name = models.CharField(max_length=150, null=True, blank=True)	# string <= 150 characters
    last_name = models.CharField(max_length=150, null=True, blank=True) # string <= 150 characters
    bio	= models.TextField(null=True, blank=True) # string
    role = models.CharField(max_length=150, choices = CHOICES, default='user')
    password = models.CharField(max_length=10, null=True, blank=True)
    confirmation_code = models.CharField(max_length=10, null=True, blank=True)


class Category(models.Model):
    pass


class Title(models.Model):
    pass


class Genre(models.Model):
    pass
