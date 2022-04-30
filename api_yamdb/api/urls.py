from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet, CategoryViewSet, TitleViewSet,
    GenreViewSet, ReviewViewSet, CommentViewSet, CodeTokenClass
)

router = DefaultRouter()
router.register(r'auth', CodeTokenClass, basename='auth_users')
router.register(r'users', UserViewSet, basename='user_for_admin')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
