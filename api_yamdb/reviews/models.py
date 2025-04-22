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

    def __str__(self):
        return self.username


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, verbose_name='Автор отзыва', 
        on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, verbose_name='Произведение', 
        on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(verbose_name='Оценка произведения', min_value=1, max_value=10)
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
    
    def __str__(self):
        return self.text
