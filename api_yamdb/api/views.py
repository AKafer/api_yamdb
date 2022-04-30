import uuid
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
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
    UserSerializer, UserForUserSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer, TitleListSerializer
)
from .permissions import (
    IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
)
from api_yamdb.settings import DOMAIN_NAME

TEMA = 'Подтверждающий код для API YAMDB'
EMAIL_FROM = f'from@{DOMAIN_NAME}'


class CodeTokenClass(viewsets.ModelViewSet):
    """Класс авторизации пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post', ], url_path='signup')
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
        Code .objects.update(
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

    @action(detail=False, methods=['post', ], url_path='token')
    def TokenGenerator(self, request):
        """Функция генерациии токена по юзернейму и коду."""
        if 'username' not in request.data \
                or 'confirmation_code' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not Code.objects.filter(
                confirmation_code=confirmation_code).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
        })


class UserViewSet(viewsets.ModelViewSet):
    """Класс представления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username')
    permission_classes = ([IsAdmin, ])
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


class MyCreateListDestroyClass(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    "Кастомный миксин класс"
    pass


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


class MyFilter(dfilters.FilterSet):
    name = dfilters.CharFilter(lookup_expr='icontains')
    genre = dfilters.CharFilter(method='get_genre_slug')
    category = dfilters.CharFilter(method='get_category_slug')

    def get_genre_slug(self, queryset, name, value):
        queryset = queryset.filter(genre__slug=value)
        return queryset

    def get_category_slug(self, queryset, name, value):
        queryset = queryset.filter(category__slug=value)
        return queryset

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления произведений"""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    serializer_class = TitleSerializer
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
