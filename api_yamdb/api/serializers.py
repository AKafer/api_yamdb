from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from django.db.models import Avg

from reviews.models import User, Review, Comment, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    #read_only_fields = ('id', 'text', 'author', 'score', 'pub_date')

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    #read_only_fields = ('id', 'text', 'author', 'score', 'pub_date')

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment
