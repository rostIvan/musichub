from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ['User']


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def has_perm(self, _perm, _obj=None):
        return self.is_active

    def has_module_perms(self, _app_label):
        return self.is_staff

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.id} | {self.email} | ' \
               f'{"admin" if self.is_admin else "user"}'
