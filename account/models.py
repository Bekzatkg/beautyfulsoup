from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


STATUS_CHOICES = (
    ('master', 'master'),
    ('customer', 'customer'),
)


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, unique=True)
    status = models.CharField(default='customer', max_length=20, choices=STATUS_CHOICES)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self):
        code = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.activation_code = code
