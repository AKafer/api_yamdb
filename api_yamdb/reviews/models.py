from pickle import FALSE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(max_length=150, unique=True) # Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
    email = models.EmailField(max_length=254, unique=True)  # required, string <email> <= 254 characters
    first_name = models.CharField(max_length=150, null=True, blank=True)	# string <= 150 characters
    last_name = models.CharField(max_length=150, null=True, blank=True) # string <= 150 characters
    bio	= models.TextField(null=True, blank=True) # string
    role = models.CharField(max_length=150, choices = CHOICES, default='user')
    password = models.CharField(max_length=10, null=True, blank=True)
    confirmation_code = models.CharField(max_length=10, null=True, blank=True)


class Category(models.Model):
    """Titles category class"""
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Краткое наименование категории',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Titles genre class"""
    name = models.CharField(
        'Жанр',
        max_length=200
    )
    slug = models.SlugField(
        'Краткое наименование жанра',
        unique=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Title class"""
    name = models.CharField(
        'Название произведения',
        null=False,
        max_length=200
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    year = models.DateTimeField(  # как проверить год? (не может быть в будущем, не м.б. отриц)
        'Год издания',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр(ы)',
        # through='Genre' # как связать?
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        blank=True,
        null=True
    )
    # rating = models.ForeignKey(
    #   Rating,
    #   null=True,
    #   blank=True
    # )

    def __str__(self):
        return f'{self.name}: общая информация'

# class Review(models.Model):
#     """
#     Отзыв на определенное произведение.
#     Выставляемая оценка от 1 до 10.
#     Рейтинг - ср.арифм. оценок.
#     Отзыв может быть только один от одного автора.
#     При удалении пользователя должны удалятся все отзывы этого пользователя.
#     При удалении произведения должны удаляться все отзывы к нему.
#     """
#     composition = models.ForeignKey(
#         Title, on_delete=models.CASCADE, related_name='reviews')
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='reviews')
#     text = models.TextField()
#     score = models.IntegerField(
#         default=1,
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(10)
#         ]
#     )
#     rating = models.IntegerField(
#         default=1,
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(10)
#         ]
#     )
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
#
#
# class Comment(models.Model):
#     """
#     Комментарий к отзыву.
#     При удалении пользователя должны удалятся все комменты этого пользователя.
#     При удалении отзыва должны удаляться все комментарии к нему.
#     """
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments')
#     review = models.ForeignKey(
#         Review, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
