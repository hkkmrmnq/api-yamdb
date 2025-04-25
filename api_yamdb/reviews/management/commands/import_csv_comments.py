import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review


User = get_user_model()


class Command(BaseCommand):
    """Импорт Комментариев из csv-файла."""

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Comment.objects.create(
                        pk=row['id'],
                        review=Review.objects.get(id=row['review_id']),
                        text=row['text'],
                        author=User.objects.get(id=row['author']),
                        pub_date=row['pub_date'],
                    )
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file_path}')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
