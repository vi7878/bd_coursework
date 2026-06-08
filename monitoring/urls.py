from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('boiler/<int:pk>/', views.BoilerDetailView.as_view(), name='boiler_detail'),
    path('incident/create/<int:boiler_id>/', views.IncidentCreateView.as_view(), name='incident_create'),
    path('incident/resolve/<int:pk>/', views.IncidentResolveView.as_view(), name='incident_resolve'),

    path('sensor/add/<int:boiler_id>/', views.SensorCreateView.as_view(), name='sensor_add'),
    path('sensor/edit/<int:pk>/', views.SensorUpdateView.as_view(), name='sensor_edit'),
    path('address/edit/<int:pk>/', views.AddressUpdateView.as_view(), name='address_edit'),
    path('boiler/status/<int:pk>/', views.BoilerStatusUpdateView.as_view(), name='boiler_status_edit'),
]
