

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_boilerroom_boiler_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Device Categories',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('green', 'Normal'), ('yellow', 'Warning'), ('red', 'Error'), ('black', 'Off')], default='green', max_length=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('boiler_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='core.boilerroom')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='monitoring.devicecategory')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('green', 'Normal'), ('yellow', 'Warning'), ('red', 'Error'), ('black', 'Off')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='monitoring.device')),
            ],
            options={
                'verbose_name_plural': 'Device Status Histories',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='core.sensor')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
