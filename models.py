# Внутренние импорты
import os
import uuid

# Импорты django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import transaction


# test

class UserManager(BaseUserManager):
    @transaction.atomic
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        except:
            raise

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    def upload_avatar_img(self, filename):
        return os.path.join("users", str(self.id), filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.TextField(default="", blank=True, unique=True)

    # chars
    phone = models.CharField(verbose_name='Номер телефона', null=True, blank=True, max_length=50, default=None)
    name = models.CharField(max_length=50, blank=True, default=None, null=True)

    # files
    avatar = models.ImageField(upload_to=upload_avatar_img, blank=True, null=True, default=None)

    # booleans
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name if self.name else str(self.phone)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.id)
        super(User, self).save(*args, **kwargs)
        return self


class OTC(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Одноразовый код"
        verbose_name_plural = "Одноразовые коды"

    def __str__(self):
        return self.code
