from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        if self.is_staff:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, _app_label):
        return self.is_staff

    @property
    def is_staff(self):
        return self.is_superuser and self.is_active

    def __str__(self):
        return f'{self.id} | {self.email}'

    class Meta:
        db_table = 'users'
