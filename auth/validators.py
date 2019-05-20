from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

__all__ = ['password_validator']


def password_validator(password):
    try:
        validate_password(password)
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)
