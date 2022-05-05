import datetime as dt
from rest_framework import serializers
from reviews.models import (
    User, Category, Genre,
    Title, Review, Comment, Code
)


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        lookup_field = ('username')
        read_only_fields = ('password',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'username не может быть me, Me, ME, mE'
            )
        return value


class TokenGeneratorSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = Code
        fields = (
            'username', 'confirmation_code'
        )


class UserForUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для юзеров."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('password', 'role')


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатора категорий."""
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = ('slug')


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатора жанров."""
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = ('slug')


class TitleSerializer(serializers.ModelSerializer):
    """Класс сериализатора произведений на добавлени, изменение, удаление."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проснись! Год не может быть больше текущего!'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Класс сериализатора произведений на выдачу"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title
        read_only_fields = ('id', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериализатора ревью."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['view'].request.user
        if (
            Review.objects.filter(title=title, author=author).exists()
            and self.context['view'].request.method == 'POST'
        ):
            raise serializers.ValidationError(
                'Вы уже писал отзыв на это. Угомонитесь!')
        return data

    def validate_score(self, value):
        if 0 < value < 11:
            return value
        raise serializers.ValidationError(
            'Проснись! Оценка должна быть от 1 до 10'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатора комментариев."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'author')
