from logging import raiseExceptions
import random
import string
import re
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from reviews.models import User
from .serializers import (
    UserSerializer,
    UserForUserSerializer
)
from .permissions import IsAdmin, IsUser

TEMA = 'Подтверждающий код для API YAMDB'
N_code_len = 20

def get_code():
    """Функция генерации кода"""
    allowedChars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(allowedChars) for _ in range(N_code_len))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username')
    permission_classes = ([IsAdmin, ])
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    
    def get_object(self):
        return get_object_or_404(
            self.queryset, username=self.kwargs["username"])

    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes=([IsAuthenticated, ]))
    def user_rool_users_detail(self, request, username=None):
        user = get_object_or_404(User, username=self.request.user)
        print(user.first_name)
        if request.method == 'PATCH':
            serializer = UserForUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserForUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
class CodGenerator(APIView):
    """Функция добавления нового пользоватля в БД, формировния и отправки кода на email"""
    def post(self, request):
        confirmation_code = get_code()
        username = request.data.get('username')
        email = request.data.get('email')
        send_mail(
            TEMA,
            confirmation_code,
            'from@example.com',
            [email],
            fail_silently=False,
        )
        if User.objects.filter(username=username, email=email).exists():
            user = get_object_or_404(User, username=username, email=email)
            user.confirmation_code = confirmation_code
            user.save()
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                User.objects.create(
                    username=username,
                    email=email,
                    confirmation_code=confirmation_code
                )
                return Response(request.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class TokenGenerator(APIView):
    """Функция генерациии токена по юзернейму и коду.
    Она должна быть из 5 строк. Но для прохождения теста пришлось написать ещё 25.
    """
    def post(self, request):
        if 'username' not in request.data or 'confirmation_code' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username=request.data['username']
        confirmation_code=request.data['confirmation_code']
        list_username = [x['username'] for x in  User.objects.all().values('username')]
        if username not in list_username:
            return Response(status=status.HTTP_404_NOT_FOUND)
        list_code = [x['confirmation_code'] for x in  User.objects.all().values('confirmation_code')]
        if confirmation_code not in list_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)   
        return Response({
                'token': str(refresh.access_token),
            })

        
