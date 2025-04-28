from django.db import models

from .constants import LIMIT_LENGTH, LIMIT_LENGTH_STR_AND_SLUG


class CategoryGenreBaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к моделям Category и Genre поля:
    наименование и идентификатор.
    """
    name = models.CharField(
        max_length=LIMIT_LENGTH,
        unique=True,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=LIMIT_LENGTH_STR_AND_SLUG,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены '
            'символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:LIMIT_LENGTH_STR_AND_SLUG]
