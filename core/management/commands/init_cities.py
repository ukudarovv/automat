"""
Management command to initialize cities.
"""
from django.core.management.base import BaseCommand
from core.models import City


class Command(BaseCommand):
    help = 'Initialize cities in database'

    def handle(self, *args, **options):
        cities_data = [
            ('Atyrau', 'Атырау'),
            ('Kulsary', 'Кульсары'),
            ('Almaty', 'Алматы'),
            ('Astana', 'Астана'),
            ('Aktau', 'Актау'),
            ('Aktobe', 'Актобе'),
            ('Shymkent', 'Шымкент'),
            ('Karaganda', 'Караганда'),
            ('Pavlodar', 'Павлодар'),
            ('Taraz', 'Тараз'),
            ('Turkestan', 'Туркестан'),
            ('Semey', 'Семей'),
            ('Oral', 'Уральск'),
            ('Kostanay', 'Костанай'),
            ('Kyzylorda', 'Кызылорда'),
            ('Taldykorgan', 'Талдыкорган'),
            ('Petropavlovsk', 'Петропавловск'),
            ('Oskemen', 'Усть-Каменогорск'),
        ]
        
        created_count = 0
        for name, name_ru in cities_data:
            city, created = City.objects.get_or_create(
                name=name,
                defaults={'name_ru': name_ru, 'is_active': True}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created city: {name}'))
            else:
                self.stdout.write(f'City already exists: {name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal cities created: {created_count}'))

