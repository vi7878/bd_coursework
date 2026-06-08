from django.db import models
from core.models import BoilerRoom, Sensor

class DeviceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'device_categories'
        verbose_name_plural = "Device Categories"

    def __str__(self):
        return self.name

class Device(models.Model):
    STATUS_CHOICES = (
        ('green', 'Норма'),
        ('yellow', 'Увага'),
        ('red', 'Аварія'),
        ('black', 'Вимкнено'),
    )
    boiler_room = models.ForeignKey(BoilerRoom, related_name='devices', on_delete=models.CASCADE)
    category = models.ForeignKey(DeviceCategory, related_name='devices', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='green')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return f"{self.name} at {self.boiler_room.name}"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='readings', on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sensor_readings'
        ordering = ['-timestamp']

class DeviceStatusHistory(models.Model):
    device = models.ForeignKey(Device, related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Device.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'device_status_history'
        ordering = ['-timestamp']
        verbose_name_plural = "Device Status Histories"
