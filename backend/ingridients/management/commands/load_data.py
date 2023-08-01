import csv

from django.core.management.base import BaseCommand

from ingridients.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Ingredient'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        self.stdout.write(
            "Заполнение модели Ingredient из csv запущено.",
            ending=''
        )
        with open(
            'ingridients/management/data/ingredients.csv', 'r'
        ) as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    if not created:
                        self.stdout.write(
                            f'Ингредиент {obj} уже существует в базе данных.',
                            ending=''
                        )
                except Exception as error:
                    self.stdout.write(
                        f'Ошибка в строке {row}: {error}',
                        ending=''
                    )

        self.stdout.write('Заполнение модели Ingredient завершено.')
