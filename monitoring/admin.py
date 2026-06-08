from django.contrib import admin
from .models import DeviceCategory, Device, SensorReading, DeviceStatusHistory

@admin.register(DeviceCategory)
class DeviceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'boiler_room', 'category', 'status', 'last_updated')
    list_filter = ('status', 'category', 'boiler_room')
    search_fields = ('name', 'boiler_room__name')

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'value', 'timestamp')
    list_filter = ('sensor', 'timestamp')

@admin.register(DeviceStatusHistory)
class DeviceStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('device', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
