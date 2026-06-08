from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Avg, Max, Min, Count, Sum, Q, OuterRef, Exists, Subquery
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from core.models import BoilerRoom, Sensor, Incident, ServiceAddress
from .models import Device, DeviceCategory, SensorReading

class EngineerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['engineer', 'admin']

class SensorCreateView(LoginRequiredMixin, EngineerRequiredMixin, CreateView):
    model = Sensor
    fields = ['name', 'sensor_type', 'current_value', 'unit']
    template_name = 'monitoring/sensor_form.html'
    
    def form_valid(self, form):
        form.instance.boiler = get_object_or_404(BoilerRoom, pk=self.kwargs['boiler_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('monitoring:boiler_detail', kwargs={'pk': self.kwargs['boiler_id']})

class SensorUpdateView(LoginRequiredMixin, EngineerRequiredMixin, UpdateView):
    model = Sensor
    fields = ['name', 'unit']
    template_name = 'monitoring/sensor_form.html'
    
    def get_success_url(self):
        return reverse_lazy('monitoring:boiler_detail', kwargs={'pk': self.object.boiler.pk})

class AddressUpdateView(LoginRequiredMixin, EngineerRequiredMixin, UpdateView):
    model = ServiceAddress
    fields = ['status', 'note']
    template_name = 'monitoring/address_form.html'
    
    def form_valid(self, form):
        if form.cleaned_data.get('status') == 'normal':
            form.instance.note = ""
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('monitoring:boiler_detail', kwargs={'pk': self.object.boiler.pk})

class BoilerStatusUpdateView(LoginRequiredMixin, EngineerRequiredMixin, UpdateView):
    model = BoilerRoom
    fields = ['status']
    template_name = 'monitoring/boiler_status_form.html'
    
    def get_success_url(self):
        return reverse_lazy('monitoring:boiler_detail', kwargs={'pk': self.object.pk})

class DashboardView(LoginRequiredMixin, EngineerRequiredMixin, ListView):
    model = BoilerRoom
    template_name = 'monitoring/dashboard.html'
    context_object_name = 'boilers'

    def get_queryset(self):
        return BoilerRoom.objects.all()

class BoilerDetailView(LoginRequiredMixin, EngineerRequiredMixin, DetailView):
    model = BoilerRoom
    template_name = 'monitoring/boiler_detail.html'
    context_object_name = 'boiler'

    def get_context_data(self, **kwargs):
        import random
        context = super().get_context_data(**kwargs)
        context['sensors'] = self.object.sensors.all()
        context['devices'] = self.object.devices.select_related('category').all()
        context['active_incidents'] = self.object.incidents.filter(is_resolved=False)
        

        schemes = [
            'schems-06.png', 'schems-08.png', 'schems-10.png', 'schems-12.png',
            'schems-14.png', 'schems-16.png', 'schems-18.png', 'schems-20.png',
            'schems-46.png', 'schems-48.png', 'schems-50.png', 'schems-52.png',
            'schems-54.png', 'schems-56.png'
        ]

        scheme_index = self.object.pk % len(schemes)
        context['scheme_image'] = f'monitoring/schemes/{schemes[scheme_index]}'


        sensor_history = {}
        for sensor in context['sensors']:
            sensor_history[sensor.id] = sensor.readings.all()[:10]
        context['sensor_history'] = sensor_history
        

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT get_avg_sensor_value(%s, 'temperature')", [self.object.pk])
            avg_temp = cursor.fetchone()[0]
        context['avg_temperature'] = avg_temp


        context['tables_data'] = {
            'pressure': {
                'return': f"{random.uniform(3.5, 4.5):.1f}",
                'supply': f"{random.uniform(5.5, 6.5):.1f}",
            },
            'heat': {
                'temp_return': f"{random.uniform(50.0, 55.0):.1f}",
                'temp_supply': f"{random.uniform(70.0, 85.0):.1f}",
                'label': 'Температура',
                'g_makeup_hr': f"{random.uniform(0.5, 1.5):.2f}",
                'g_makeup_day': f"{random.uniform(10.0, 20.0):.1f}",
                'g_heat_hr': f"{random.uniform(2.0, 4.0):.2f}",
                'g_heat_day': f"{random.uniform(40.0, 60.0):.1f}",
                'g_supply_hr': f"{random.uniform(10.0, 15.0):.1f}",
                'g_supply_day': f"{random.uniform(200.0, 300.0):.1f}",
            },
            'electricity': {
                'power_active': f"{random.uniform(10.0, 25.0):.1f}",
                'power_reactive': f"{random.uniform(1.0, 5.0):.1f}",
                'cons_day': f"{random.uniform(100.0, 150.0):.1f}",
                'cons_month': f"{random.uniform(1500.0, 2500.0):.1f}",
            },
            'gas': {
                'cons_day': f"{random.uniform(40.0, 80.0):.1f}",
                'cons_month': f"{random.uniform(800.0, 1500.0):.1f}",
                'pressure_day': f"{random.uniform(1.5, 2.5):.2f}",
                'pressure_month': f"{random.uniform(1.5, 2.5):.2f}",
            }
        }
        
        return context

class IncidentCreateView(LoginRequiredMixin, EngineerRequiredMixin, CreateView):
    model = Incident
    template_name = 'monitoring/incident_form.html'
    fields = ['description', 'affected_addresses']
    
    def form_valid(self, form):
        boiler = get_object_or_404(BoilerRoom, pk=self.kwargs['boiler_id'])
        form.instance.boiler = boiler
        response = super().form_valid(form)
        

        boiler.status = 'error'
        boiler.save()
        

        for address in form.instance.affected_addresses.all():
            address.status = 'disconnected'
            address.note = f"Ручне відключення: {form.instance.description}"
            address.save()
            
        return response
    
    def get_success_url(self):
        return reverse_lazy('monitoring:boiler_detail', kwargs={'pk': self.kwargs['boiler_id']})

class IncidentResolveView(LoginRequiredMixin, EngineerRequiredMixin, UpdateView):
    model = Incident
    template_name = 'monitoring/incident_resolve.html'
    fields = []

    def post(self, request, *args, **kwargs):
        incident = self.get_object()
        incident.is_resolved = True
        incident.end_time = timezone.now()
        incident.save()
        

        if not incident.boiler.incidents.filter(is_resolved=False).exists():
            incident.boiler.status = 'active'
            incident.boiler.save()
            

        for address in incident.affected_addresses.all():
            address.status = 'normal'
            address.note = "Систему відновлено інженером"
            address.save()
            
        return redirect('monitoring:boiler_detail', pk=incident.boiler.pk)
