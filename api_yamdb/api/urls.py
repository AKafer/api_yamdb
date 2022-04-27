from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet, code_generate,
    ReviewViewSet,
    CommentViewSet,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
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
    path('v1/auth/signup/', code_generate),
]