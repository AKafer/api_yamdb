from django.shortcuts import render
from rest_framework import viewsets

from .models import User, Category, Title, Genre
from .serializers import (CategorySerializer, TitleSerializer, GenreSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass
