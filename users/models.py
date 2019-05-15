from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ['User']


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False)

    def __str__(self):
        return f'{self.id}, {self.username}, {self.email}'
