import yagmail
import random
import string
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, filters, mixins
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework import status

# from .permissions import IsOwnerOrReadOnly
from reviews.models import User
from .serializers import (
    UserSerializer, MyTokenObtainPairSerializerNoPassword
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CODGenerator(APIView):
    def post(self, request):
        N = 20
        allowedChars = string.ascii_letters + string.digits + string.punctuation
        confirmation_code = ''.join(random.choice(allowedChars) for _ in range(N))
        yag = yagmail.SMTP(user="akafer82@yandex.ru", password="sskssk82", host='smtp.yandex.ru')
        tema = 'Проверочный код'
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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializerNoPassword
