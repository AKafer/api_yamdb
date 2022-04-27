from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Category, Title, Genre
from .serializers import (CategorySerializer, TitleSerializer, GenreSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (OwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter, )  #DjangoFilterBackend
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (OwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('category', 'genre', 'name', 'year')
