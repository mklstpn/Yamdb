from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRole.CHOICES,
                            verbose_name='user role', default=UserRole.USER)
    bio = models.TextField(blank=True, null=True, verbose_name='biography')
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name')
    email = models.EmailField(
        blank=False, unique=True, max_length=254, verbose_name='email address')
    confirmation_code = models.CharField(
        blank=True, max_length=10, verbose_name='confirmation code')

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser
