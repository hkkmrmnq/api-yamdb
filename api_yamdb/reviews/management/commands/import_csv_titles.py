import csv

from django.core.management.base import BaseCommand

from reviews.models import Title, Category


class Command(BaseCommand):
    """Импорт Произведений из csv-файла."""

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Title.objects.create(
                        pk=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get(id=row['category']),
                    )
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file_path}')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
