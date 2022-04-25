from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserViewSet, CODGenerator,
    MyTokenObtainPairView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CODGenerator.as_view()),
    path('v1/auth/token/', MyTokenObtainPairView.as_view()),
]