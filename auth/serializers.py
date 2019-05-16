from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth.fields import PasswordField

__all__ = ['SignUpSerializer']

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
