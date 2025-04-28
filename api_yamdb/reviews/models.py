from django.contrib.auth import get_user_model
from django.db import models

from .constants import LIMIT_LENGTH, LIMIT_LENGTH_STR_AND_SLUG
from .validators import validate_year

User = get_user_model()


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


class Category(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LIMIT_LENGTH_STR_AND_SLUG]


class Genre(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LIMIT_LENGTH_STR_AND_SLUG]


class Title(models.Model):
    name = models.CharField(
        max_length=LIMIT_LENGTH,
        verbose_name='Наименование'
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles',
        through='GenreTitle',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category', 'year'],
                name='unique_name_category_year',
            )
        ]

    def __str__(self):
        return self.name[:LIMIT_LENGTH_STR_AND_SLUG]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        related_name='genre_title',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='genre_title',
    )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'], name='unique_genre_title'
            )
        ]

    def __str__(self):
        return (f'{self.title[:LIMIT_LENGTH_STR_AND_SLUG]}'
                '- {self.genre[:LIMIT_LENGTH_STR_AND_SLUG]}')


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        choices=[(i, str(i)) for i in range(1, 11)],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:LIMIT_LENGTH_STR_AND_SLUG]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LIMIT_LENGTH_STR_AND_SLUG]
