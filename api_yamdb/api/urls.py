from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet, code_generate
)


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', code_generate),
]