from pickle import NONE
import yagmail
import random
import string
import os
from dotenv import load_dotenv
from rest_framework.views import APIView

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response # Импортировали класс Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# from .permissions import IsOwnerOrReadOnly
from reviews.models import User
from .serializers import (
    UserSerializer,
    UserForUserSerializer
)


load_dotenv()
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
N_code_len = 20
allowedChars = string.ascii_letters + string.digits + string.punctuation

def get_code():
    allowedChars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(allowedChars) for _ in range(N_code_len))



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

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

    """
    @action(detail=False, methods=['get', 'patch'], url_path='me/')
    def user_rool_users_detail(self, request, username=None):
        print('111111111111111111111111111111111111111111111111111111111111111111')
        user = get_object_or_404(User, username = self.request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    """

    @action(detail=False, methods=['get', 'delete', 'patch'], url_path=r'(?P<username>\w+)')
    def admin_rool_users_detail(self, request, username=None):

        user = get_object_or_404(User, username=username)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                if 'role' in  self.request.data:
                    if self.request.data['role'] == 'moderator':
                        serializer.save(is_staff=True, is_superuser=False)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    elif self.request.data['role'] == 'admin':
                        serializer.save(is_staff=True, is_superuser=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        serializer.save(is_staff=False, is_superuser=False)
                        return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        serializer = self.get_serializer(user)
        return Response(serializer.data)



class CODGenerator(APIView):
    def post(self, request):
        confirmation_code = get_code()
        yag = yagmail.SMTP(user="akafer82@yandex.ru", password=EMAIL_PASSWORD, host='smtp.yandex.ru')
        tema = 'Подтверждающий код для API YAMDB'
        username = request.data.get('username')
        email = request.data.get('email')
        yag.send(['akafer@mail.ru'], tema, confirmation_code)
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


class APICat(APIView):
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
        user.save()
        return Response({
            'token': str(refresh.access_token),
        })


