import yagmail
import random
import string
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

import os

from reviews.models import User
from .serializers import (
    UserSerializer,
    UserForUserSerializer
)


load_dotenv()
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TEMA = 'Подтверждающий код для API YAMDB'
N_code_len = 20

def get_code():
    allowedChars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(allowedChars) for _ in range(N_code_len))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username')
    permission_classes=[IsAdminUser]
    pagination_class = PageNumberPagination

    def get_object(self):
        return get_object_or_404(self.queryset, username=self.kwargs["username"])

    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes=[IsAuthenticated])
    def user_rool_users_detail(self, request, username=None):
        user = get_object_or_404(User, username = self.request.user)
        if request.method == 'PATCH':
            serializer = UserForUserSerializer(user, data = request.data, partial=True)
            if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserForUserSerializer(user)            
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def perform_create(self, serializer):
        print(self.request.user)
        if 'role' in  self.request.data:
            if self.request.data['role'] == 'moderator':
                serializer.save(is_staff=True, is_superuser=False)
            elif self.request.data['role'] == 'admin':
                serializer.save(is_staff=True, is_superuser=True)
            else:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

    def perform_update(self, serializer):
        print(self.request.user)
        if 'role' in  self.request.data:
            if self.request.data['role'] == 'moderator':
                serializer.save(is_staff=True, is_superuser=False)
            elif self.request.data['role'] == 'admin':
                serializer.save(is_staff=True, is_superuser=True)
            else:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()


class CodGenerator(APIView):
    def post(self, request):
        confirmation_code = get_code()
        yag = yagmail.SMTP(user="akafer82@yandex.ru", password=EMAIL_PASSWORD, host='smtp.yandex.ru')
        username = request.data.get('username')
        email = request.data.get('email')
        yag.send([email], TEMA, confirmation_code)
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username, email=email)
            user.confirmation_code = confirmation_code
            user.save()
            return Response(request.data, status=status.HTTP_200_OK) 
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():    
                User.objects.create(username=username, email=email, confirmation_code=confirmation_code)
                return Response(request.data, status=status.HTTP_200_OK) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenGenerator(APIView):
    def post(self, request):
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code
        )
        print(user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
        })


