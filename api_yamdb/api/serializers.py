from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import PasswordField

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        lookup_field = ('username')
        read_only_fields = ('password',)


class UserForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)
        read_only_fields = ('password',)