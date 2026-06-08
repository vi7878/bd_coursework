from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Адміністратор'),
        ('engineer', 'Інженер'),
        ('client', 'Клієнт'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

class BoilerRoom(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активний'),
        ('maintenance', 'Обслуговування'),
        ('error', 'Помилка'),
    )
    TYPE_CHOICES = (
        ('scheme_1', 'Схема 1 (a-d)'),
        ('scheme_2', 'Схема 2 (a-d)'),
        ('scheme_9', 'Схема 9 (a-d)'),
        ('scheme_10', 'Схема 10 / 10c'),
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    boiler_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='scheme_1')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        db_table = 'boiler_rooms'

    def __str__(self):
        return self.name

class Sensor(models.Model):
    SENSOR_TYPES = (
        ('temperature', 'Температура'),
        ('pressure', 'Тиск'),
        ('flow', 'Витрата'),
    )
    boiler = models.ForeignKey(BoilerRoom, related_name='sensors', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    current_value = models.FloatField()
    unit = models.CharField(max_length=20)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sensors'

    def __str__(self):
        return f"{self.name} ({self.boiler.name})"

class ServiceAddress(models.Model):
    STATUS_CHOICES = (
        ('normal', 'Норма'),
        ('no_heating', 'Немає опалення'),
        ('no_hot_water', 'Немає гарячої води'),
        ('disconnected', 'Відключено'),
    )
    boiler = models.ForeignKey(BoilerRoom, related_name='service_addresses', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    note = models.TextField(blank=True, null=True, verbose_name="Коментар інженера")

    class Meta:
        db_table = 'service_addresses'

    def __str__(self):
        return f"{self.city}, {self.street} {self.building}"

class Incident(models.Model):
    boiler = models.ForeignKey(BoilerRoom, related_name='incidents', on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Опис інциденту")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    affected_addresses = models.ManyToManyField(ServiceAddress, blank=True, verbose_name="Адреси, що потрапили під відключення")

    class Meta:
        db_table = 'incidents'

    def __str__(self):
        return f"Аварія на {self.boiler.name} ({self.start_time})"
