from django.core.management.base import BaseCommand
from core.models import User, BoilerRoom, Sensor, ServiceAddress, Incident
from monitoring.models import DeviceCategory, Device, SensorReading
import random

class Command(BaseCommand):
    help = 'Populate the database with mock data for visualization'

    def handle(self, *args, **kwargs):

        BoilerRoom.objects.all().delete()
        DeviceCategory.objects.all().delete()
        User.objects.filter(username='engineer').delete()


        User.objects.create_user('engineer', 'eng@example.com', 'engpass', role='engineer')
        self.stdout.write(self.style.SUCCESS('Created engineer user'))


        categories_data = [
            {'name': 'Насос', 'slug': 'pump'},
            {'name': 'Регулятор тиску', 'slug': 'pressure-regulator'},
            {'name': 'Регулятор температури', 'slug': 'temp-regulator'},
            {'name': 'Клапан', 'slug': 'valve'},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, created = DeviceCategory.objects.get_or_create(slug=cat_data['slug'], defaults={'name': cat_data['name']})
            categories[cat_data['slug']] = cat

        streets = [
            'Пастерівська', 'Максима Залізняка', 'Смілянська', 
            'Хоменка', 'Оборонна', 'Надпільна', 
            'Благовісна', 'Гоголя', 'Хрещатик'
        ]

        types = ['scheme_1', 'scheme_2', 'scheme_9', 'scheme_10']


        all_boilers = []
        for i in range(1, 19):
            street = random.choice(streets)
            building = random.randint(1, 100)
            boiler_type = random.choice(types)
            status = 'active'
            
            if random.random() > 0.9:
                status = random.choice(['maintenance', 'error'])

            boiler = BoilerRoom.objects.create(
                name=f'Котельня №{i}',
                address=f'вул. {street}, {building}',
                status=status,
                boiler_type=boiler_type
            )
            all_boilers.append(boiler)
            self.stdout.write(self.style.SUCCESS(f'Created boiler {boiler.name}'))


            for slug, cat in categories.items():
                device_status = 'green'
                if status == 'error':
                    device_status = random.choice(['red', 'black', 'yellow'])
                elif status == 'maintenance':
                    device_status = 'black'
                else:
                    device_status = random.choice(['green', 'green', 'green', 'yellow'])
                    
                Device.objects.create(
                    boiler_room=boiler,
                    category=cat,
                    name=f"{cat.name} 1",
                    status=device_status
                )


            sensor_configs = [
                {'name': 'Датчик температури (подача)', 'type': 'temperature', 'unit': '°C', 'min': 60, 'max': 90},
                {'name': 'Датчик температури (зворот)', 'type': 'temperature', 'unit': '°C', 'min': 40, 'max': 55},
                {'name': 'Датчик тиску (вхід)', 'type': 'pressure', 'unit': 'Bar', 'min': 3, 'max': 5},
                {'name': 'Датчик тиску (вихід)', 'type': 'pressure', 'unit': 'Bar', 'min': 5, 'max': 8},
            ]
            for config in sensor_configs:
                val = round(random.uniform(config['min'], config['max']), 1)
                sensor = Sensor.objects.create(
                    boiler=boiler,
                    name=config['name'],
                    sensor_type=config['type'],
                    unit=config['unit'],
                    current_value=val
                )

                for _ in range(20):
                    SensorReading.objects.create(
                        sensor=sensor,
                        value=round(val + random.uniform(-2, 2), 1)
                    )


        used_addresses = set()
        for boiler in all_boilers:
            num_addresses = random.randint(3, 6)
            count = 0
            while count < num_addresses:
                street = random.choice(streets)
                building = str(random.randint(1, 150))
                

                if (street, building) not in used_addresses:
                    ServiceAddress.objects.create(
                        boiler=boiler,
                        city='Черкаси',
                        street=street,
                        building=building,
                        status='normal'
                    )
                    used_addresses.add((street, building))
                    count += 1
            

            if random.random() > 0.5:
                Incident.objects.create(
                    boiler=boiler,
                    description=f"Профілактичні роботи на {boiler.name}",
                    is_resolved=random.choice([True, False])
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(used_addresses)} unique service addresses'))
