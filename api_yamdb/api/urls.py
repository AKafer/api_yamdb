from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet, get_me,
    CODGenerator, APICat
)


router = DefaultRouter()
# router.register(r'users/me', MeViewSet, basename='user_for_me')
router.register(r'users', UserViewSet, basename='user_for_admin')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CODGenerator.as_view()),
    path('v1/auth/token/', APICat.as_view()),
    path('v1/users/me/', get_me),
]
