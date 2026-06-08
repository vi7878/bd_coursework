from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BoilerRoom, Sensor, ServiceAddress, Incident

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

@admin.register(BoilerRoom)
class BoilerRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'address')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'boiler', 'sensor_type', 'current_value', 'unit', 'last_updated')
    list_filter = ('sensor_type', 'boiler')
    search_fields = ('name', 'boiler__name')

@admin.register(ServiceAddress)
class ServiceAddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'building', 'boiler', 'status')
    list_filter = ('status', 'boiler', 'city')
    search_fields = ('street', 'building')

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('boiler', 'start_time', 'end_time', 'is_resolved')
    list_filter = ('is_resolved', 'boiler')
    search_fields = ('description', 'boiler__name')
    filter_horizontal = ('affected_addresses',)
