from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = [
        (Role.USER.value, 'Пользователь'),
        (Role.MODERATOR.value, 'Модератор'),
        (Role.ADMIN.value, 'Администратор'),
    ]
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=Role.USER.value,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты', max_length=254, unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
