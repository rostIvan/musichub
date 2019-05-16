from rest_framework import serializers

from auth.validators import password_validator

__all__ = ['PasswordField']


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = kwargs.get('write_only', True)
        kwargs['required'] = kwargs.get('required', True)
        kwargs['validators'] = kwargs.get('validators', [password_validator])
        kwargs['style'] = kwargs.get('style', {'input_type': 'password',
                                               'placeholder': 'Password'})
        kwargs['help_text'] = kwargs.get('help_text')
        super().__init__(**kwargs)
