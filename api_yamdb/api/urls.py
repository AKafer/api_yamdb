from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet,
    CodGenerator, TokenGenerator
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user_for_admin')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CodGenerator.as_view()),
    path('v1/auth/token/', TokenGenerator.as_view()),
]
