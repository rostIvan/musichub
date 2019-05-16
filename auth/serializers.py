from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth.fields import PasswordField

__all__ = ['SignUpSerializer']


class SignUpSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
