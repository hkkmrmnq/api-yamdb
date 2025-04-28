import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


User = get_user_model()


class Command(BaseCommand):
    """Импорт данных из csv-файлов."""

    def _import_user(self, row):
        User.objects.create(
            pk=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )

    def _import_category(self, row):
        Category.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def _import_genre(self, row):
        Genre.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def _import_title(self, row):
        Title.objects.create(
            pk=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category']),
        )

    def _import_genre_title(self, row):
        GenreTitle.objects.create(
            pk=row['id'],
            genre=Genre.objects.get(id=row['genre_id']),
            title=Title.objects.get(id=row['title_id']),
        )

    def _import_review(self, row):
        Review.objects.create(
            pk=row['id'],
            title=Title.objects.get(id=row['title_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        )

    def _import_comments(self, row):
        Comment.objects.create(
            pk=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=row['pub_date'],
        )

    def handle(self, *args, **kwargs):
        files_paths = (
            (self._import_user, 'static/data/users.csv'),
            (self._import_category, 'static/data/category.csv'),
            (self._import_genre, 'static/data/genre.csv'),
            (self._import_title, 'static/data/titles.csv'),
            (self._import_genre_title, 'static/data/genre_title.csv'),
            (self._import_review, 'static/data/review.csv'),
            (self._import_comments, 'static/data/comments.csv'),
        )

        for method, path in files_paths:
            try:
                with open(path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            method(row)
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'Error importing data: {e}')
                            )
                    self.stdout.write(self.style.SUCCESS(f'{path} processed.'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f'File not found: {path}'))
