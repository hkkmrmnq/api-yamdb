import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Review, Title


User = get_user_model()


class Command(BaseCommand):
    """Импорт Отзывов из csv-файла."""

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Review.objects.create(
                        pk=row['id'],
                        title=Title.objects.get(id=row['title_id']),
                        text=row['text'],
                        author=User.objects.get(id=row['author']),
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file_path}')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
