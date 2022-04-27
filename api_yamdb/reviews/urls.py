from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
#
# router = DefaultRouter()
# router.register(r'categories', views.CategoryViewSet, basename='categories')
# router.register(r'titles', views.TitleViewSet, basename='titles')
# router.register(r'genres', views.GenreViewSet, basename='genres')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
