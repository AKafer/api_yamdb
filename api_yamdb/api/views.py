import yagmail
from rest_framework import viewsets, filters, mixins
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response

# from .permissions import IsOwnerOrReadOnly
from reviews.models import User
from .serializers import (
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        confirmation_code = 'proba'
        serializer.save(confirmation_code=confirmation_code)
    
    
    # permission_classes = (IsOwnerOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    # def perform_create(self, serializer):
        # serializer.save(author=self.request.user)

@api_view(['POST']) 
def code_generate(request):
    yag = yagmail.SMTP( user="akafer82@yandex.ru", password="sskssk82", host='smtp.yandex.ru')
    tema = 'Проверочный код'
    contents = ['Здесь будет код']
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        yag.send(['akafer@mail.ru'], tema, contents)
        User.objects.filter(username=username, email=email).confirmation_code = 'jjjj'
        return Response({'data': request.data})
    return Response({'message': 'Данные некорректны', 'data': request.data})
