import uuid
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as dfilters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import (
    User, Code, Category, Genre,
    Title, Review
)
from .serializers import (
    UserSerializer, UserForUserSerializer, TokenGeneratorSerialiser,
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer, TitleListSerializer
)
from .permissions import (
    IsAdmin, IsAdminOrReadOnly,
    IsOwnerOrReadOnly, NobodyAllow
)
from .mixin import MyCreateListDestroyClass
from .filters import MyFilter
from api_yamdb.settings import DOMAIN_NAME

TEMA = 'Подтверждающий код для API YAMDB'
EMAIL_FROM = f'from@{DOMAIN_NAME}'


class CodeTokenClass(viewsets.ModelViewSet):
    """Класс авторизации пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (NobodyAllow, )

    @action(
        detail=False, methods=['post'],
        url_path='signup', permission_classes=(AllowAny, )
    )
    def CodGenerator(self, request):
        """Функция генерациии кода по юзернейму и email."""
        confirmation_code = str(uuid.uuid4())
        username = request.data.get('username')
        email = request.data.get('email')
        serializer = self.get_serializer(data=request.data)
        if not User.objects.filter(username=username, email=email).exists():
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create(username=username, email=email)
                Code.objects.create(
                    user=user,
                    confirmation_code=confirmation_code
                )
                send_mail(
                    TEMA,
                    confirmation_code,
                    EMAIL_FROM,
                    [email],
                    fail_silently=False,
                )
                return Response(request.data, status=status.HTTP_200_OK)
        user = get_object_or_404(User, username=username, email=email)
        Code.objects.update(
            user=user,
            confirmation_code=confirmation_code
        )
        send_mail(
            TEMA,
            confirmation_code,
            EMAIL_FROM,
            [email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['post'],
        url_path='token', permission_classes=(AllowAny, )
    )
    def TokenGenerator(self, request):
        """Функция генерациии токена по юзернейму и коду."""
        serializer = TokenGeneratorSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user_valid = get_object_or_404(User, username=username)
        try:
            user = Code.objects.get(
                user=user_valid,
                confirmation_code=confirmation_code
            )
        except Code.DoesNotExist:
            return Response(
                {'message': 'Проверь confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
        })


class UserViewSet(viewsets.ModelViewSet):
    """Класс представления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username')
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        return get_object_or_404(
            self.queryset, username=self.kwargs["username"])

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', permission_classes=(IsAuthenticated, )
    )
    def user_rool_users_detail(self, request, username=None):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            serializer = UserForUserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserForUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(MyCreateListDestroyClass):
    """Класс представления категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = ('slug')

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class GenreViewSet(MyCreateListDestroyClass):
    """Класс представления жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filterset_fields = ('slug',)
    lookup_field = ('slug')
    ordering = ('slug',)

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления произведений"""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = MyFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс представления ревью."""
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            title=title,
            author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Класс представления комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            review=review,
            author=self.request.user,
        )
