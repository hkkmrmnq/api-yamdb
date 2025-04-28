from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_username
from reviews.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=max([len(role[0]) for role in Role.choices]),
        choices=Role,
        default=Role.USER,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    def __str__(self):
        return self.username
