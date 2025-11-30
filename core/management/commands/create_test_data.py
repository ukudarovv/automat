"""
Management command to create test data for schools and instructors.
"""
from django.core.management.base import BaseCommand
from core.models import City, School, Instructor, User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates test data for schools and instructors'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Get or create cities
        cities_data = {
            'Atyrau': {'lat': 47.1, 'lon': 51.9},
            'Almaty': {'lat': 43.2, 'lon': 76.9},
            'Astana': {'lat': 51.1, 'lon': 71.4},
            'Shymkent': {'lat': 42.3, 'lon': 69.6},
            'Aktau': {'lat': 43.6, 'lon': 51.2},
        }
        
        cities = {}
        for city_name, coords in cities_data.items():
            city, created = City.objects.get_or_create(
                name=city_name,
                defaults={
                    'is_active': True,
                    'latitude': coords['lat'],
                    'longitude': coords['lon']
                }
            )
            cities[city_name] = city
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created city: {city_name}'))
            else:
                self.stdout.write(f'City already exists: {city_name}')
        
        # Create test schools
        schools_data = [
            {
                'name': 'Автошкола "Мастер"',
                'city': 'Atyrau',
                'address': 'ул. Абая, 15',
                'rating': 4.8,
                'trust_index': 95.0,
            },
            {
                'name': 'Автошкола "Профи"',
                'city': 'Atyrau',
                'address': 'пр. Азаттык, 45',
                'rating': 4.6,
                'trust_index': 92.0,
            },
            {
                'name': 'Автошкола "Драйв"',
                'city': 'Almaty',
                'address': 'ул. Абая, 100',
                'rating': 4.9,
                'trust_index': 98.0,
            },
            {
                'name': 'Автошкола "Старт"',
                'city': 'Almaty',
                'address': 'пр. Достык, 200',
                'rating': 4.5,
                'trust_index': 90.0,
            },
            {
                'name': 'Автошкола "Эксперт"',
                'city': 'Astana',
                'address': 'ул. Кенесары, 50',
                'rating': 4.7,
                'trust_index': 93.0,
            },
            {
                'name': 'Автошкола "Успех"',
                'city': 'Shymkent',
                'address': 'ул. Тауке хана, 30',
                'rating': 4.4,
                'trust_index': 88.0,
            },
        ]
        
        for school_data in schools_data:
            city = cities[school_data['city']]
            # Create user for school
            # Clean username from special characters
            name_clean = school_data['name'].lower().replace(' ', '_')
            name_clean = name_clean.replace('"', '').replace("'", '')
            name_clean = name_clean.replace('\u00AB', '').replace('\u00BB', '')  # « and »
            username = f"school_{name_clean}"
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'role': 'school',
                    'email': f'{username}@example.com'
                }
            )
            
            # Check if school already exists
            existing_school = School.objects.filter(name=school_data['name'], city=city).first()
            if existing_school:
                self.stdout.write(f'School already exists: {school_data["name"]}')
            else:
                school = School.objects.create(
                    user=user,
                    name=school_data['name'],
                    city=city,
                    address=school_data['address'],
                    rating=school_data['rating'],
                    trust_index=school_data['trust_index'],
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created school: {school_data["name"]} in {school_data["city"]}'))
        
        # Create test instructors
        instructors_data = [
            {
                'name': 'Иван Петров',
                'city': 'Atyrau',
                'phone': '+77001234580',
                'auto_type': 'automatic',
                'rating': 4.9,
            },
            {
                'name': 'Мария Сидорова',
                'city': 'Atyrau',
                'phone': '+77001234581',
                'auto_type': 'manual',
                'rating': 4.8,
            },
            {
                'name': 'Алексей Козлов',
                'city': 'Atyrau',
                'phone': '+77001234582',
                'auto_type': 'automatic',
                'rating': 4.7,
            },
            {
                'name': 'Елена Нурланова',
                'city': 'Almaty',
                'phone': '+77001234583',
                'auto_type': 'automatic',
                'rating': 5.0,
            },
            {
                'name': 'Дмитрий Абдулов',
                'city': 'Almaty',
                'phone': '+77001234584',
                'auto_type': 'manual',
                'rating': 4.6,
            },
            {
                'name': 'Анна Бекова',
                'city': 'Astana',
                'phone': '+77001234585',
                'auto_type': 'automatic',
                'rating': 4.8,
            },
            {
                'name': 'Сергей Темиров',
                'city': 'Shymkent',
                'phone': '+77001234586',
                'auto_type': 'manual',
                'rating': 4.5,
            },
        ]
        
        for instructor_data in instructors_data:
            city = cities[instructor_data['city']]
            # Create user for instructor
            username = f"instructor_{instructor_data['name'].lower().replace(' ', '_')}"
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'role': 'instructor',
                    'email': f'{username}@example.com'
                }
            )
            
            # Check if instructor already exists
            existing_instructor = Instructor.objects.filter(
                name=instructor_data['name'],
                city=city,
                auto_type=instructor_data['auto_type']
            ).first()
            
            if existing_instructor:
                self.stdout.write(f'Instructor already exists: {instructor_data["name"]}')
            else:
                instructor = Instructor.objects.create(
                    user=user,
                    name=instructor_data['name'],
                    city=city,
                    auto_type=instructor_data['auto_type'],
                    phone=instructor_data['phone'],
                    rating=instructor_data['rating'],
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Created instructor: {instructor_data["name"]} ({instructor_data["auto_type"]}) in {instructor_data["city"]}'
                ))
        
        self.stdout.write(self.style.SUCCESS('\nTest data created successfully!'))
        self.stdout.write(f'Created/Updated: {len(cities)} cities, {len(schools_data)} schools, {len(instructors_data)} instructors')

