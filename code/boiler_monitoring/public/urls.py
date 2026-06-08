from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('addresses/', views.AllAddressesView.as_view(), name='all_addresses'),
    path('search/', views.SearchView.as_view(), name='search'),
]
