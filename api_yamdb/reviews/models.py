from django.db import models


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
