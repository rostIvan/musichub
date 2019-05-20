from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

__all__ = ['password_validator']


def _catch_password_errors(password):
    errors = []
    try:
        validate_password(password)
    except exceptions.ValidationError as e:
        errors.extend(e.messages)
    return errors


def password_validator(password):
    errors = _catch_password_errors(password)
    if errors:
        raise serializers.ValidationError(errors)
