import yagmail
from rest_framework import viewsets, filters, mixins
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response

# from .permissions import IsOwnerOrReadOnly
from reviews.models import User, Title, Review
from .serializers import (
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
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
        user = User.objects.get(username=username, email=email)
        print(user.confirmation_code)
        user.confirmation_code = 'jjjj'
        user.save()
        print(user.confirmation_code)
        return Response({'data': request.data})
    return Response({'message': 'Данные некорректны', 'data': request.data})


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = [
     #   permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        score_avg = round(title.reviews.all().aggregate(Avg('score')))
        serializer.save(
            title_id=title.id,
            author=self.request.user,
            score=score_avg)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    #permission_classes = [
       # permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.review.filter(pk=self.kwargs.get('review_id'))
        return review.comments.all()

