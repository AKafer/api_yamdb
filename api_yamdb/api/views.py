import random
import string
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import (
    User, Category, Genre,
    Title, Review
)
from .serializers import (
    UserSerializer, UserForUserSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer, TitleCreateSerializer,
    ReviewSerializer, CommentSerializer
)
from .permissions import (
    IsAdmin, IsAdminOrReadOnly, IsOwnerModerator
)

TEMA = 'Подтверждающий код для API YAMDB'
N_code_len = 20


def get_code():
    """Функция генерации кода"""
    allowedChars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(allowedChars) for _ in range(N_code_len))


class CodGenerator(APIView):
    """Функция добавления нового пользоватля в БД,
    формировния и отправки кода на email.
    """
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
    Она должна быть из 5 строк.
    Но для прохождения теста пришлось написать ещё 25.
    """
    def post(self, request):
        if 'username' not in request.data \
                or 'confirmation_code' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        db_usernames = User.objects.all().values('username')
        list_username = [x['username'] for x in db_usernames]
        if username not in list_username:
            return Response(status=status.HTTP_404_NOT_FOUND)
        db_codes = User.objects.all().values('confirmation_code')
        list_code = [x['confirmation_code'] for x in db_codes]
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


class UserViewSet(viewsets.ModelViewSet):
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
        url_path='me', permission_classes=([IsAuthenticated, ])
    )
    def user_rool_users_detail(self, request, username=None):
        user = get_object_or_404(User, username=self.request.user)
        print(user.first_name)
        if request.method == 'PATCH':
            serializer = UserForUserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserForUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ([IsAdminOrReadOnly, ])
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = ('slug')

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ([IsAdminOrReadOnly, ])
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = ('slug')

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ([IsAdminOrReadOnly, ])
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    pagination_class = PageNumberPagination
    filterset_fields = ('category', 'genre__slug', 'year', 'name')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ([IsAuthenticatedOrReadOnly, ])

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # score_avg = round(title.reviews.all().aggregate(Avg('score')))
        serializer.save(
            title=title,
            author=self.request.user,
            # score=score_avg
        )

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'destroy':
            return (IsOwnerModerator(), )
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ([IsAuthenticatedOrReadOnly, ])

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            review=review,
            author=self.request.user,
        )

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'destroy':
            return (IsOwnerModerator(), )
        return super().get_permissions()
