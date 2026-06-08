from django.core.management.base import BaseCommand
from core.models import BoilerRoom, Sensor, ServiceAddress, Incident
import time
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Simulates critical events every 30 seconds'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Simulation started. Press Ctrl+C to stop.'))
        
        while True:

            boiler = random.choice(BoilerRoom.objects.all())
            

            sensor = boiler.sensors.filter(sensor_type__in=['temperature', 'pressure']).first()
            if not sensor:
                continue

            original_value = sensor.current_value
            original_boiler_status = boiler.status
            

            critical_val = 110.0 if sensor.sensor_type == 'temperature' else 12.0
            sensor.current_value = critical_val
            sensor.save()
            
            boiler.status = 'error'
            boiler.save()


            desc = f"КРИТИЧНА ПОМИЛКА: {sensor.name} досяг значення {critical_val} {sensor.unit}!"
            incident = Incident.objects.create(
                boiler=boiler,
                description=desc,
                is_resolved=False
            )
            

            addresses = boiler.service_addresses.all()
            old_statuses = {addr.id: addr.status for addr in addresses}
            
            new_status = random.choice(['no_heating', 'no_hot_water', 'disconnected'])
            for addr in addresses:
                addr.status = new_status
                addr.note = f"Автоматичне відключення через аварію на котельні ({sensor.name})"
                addr.save()
            
            incident.affected_addresses.set(addresses)
            
            self.stdout.write(self.style.WARNING(f'CRITICAL EVENT at {boiler.name}: {desc}'))
            self.stdout.write(f'Affected {len(addresses)} addresses for 60 seconds...')


            time.sleep(60)


            sensor.current_value = original_value
            sensor.save()
            
            boiler.status = 'active'
            boiler.save()
            
            incident.is_resolved = True
            incident.end_time = timezone.now()
            incident.save()
            
            for addr in addresses:
                addr.status = old_statuses.get(addr.id, 'normal')
                addr.note = "Систему відновлено автоматично"
                addr.save()

            self.stdout.write(self.style.SUCCESS(f'System at {boiler.name} restored to normal.'))
            

            self.stdout.write('Waiting 30 seconds for next cycle...')
            time.sleep(30)
