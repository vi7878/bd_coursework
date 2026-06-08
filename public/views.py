from django.views.generic import TemplateView, ListView
from core.models import ServiceAddress, Incident

class HomeView(TemplateView):
    template_name = 'public/home.html'

class AllAddressesView(ListView):
    model = ServiceAddress
    template_name = 'public/all_addresses.html'
    context_object_name = 'addresses'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = ServiceAddress.objects.all().order_by('street', 'building')
        if query:
            queryset = queryset.filter(
                street__icontains=query
            ) | queryset.filter(
                building__icontains=query
            )
        return queryset

class SearchView(ListView):
    model = ServiceAddress
    template_name = 'public/search_results.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return ServiceAddress.objects.filter(
                street__icontains=query
            ) | ServiceAddress.objects.filter(
                city__icontains=query
            )
        return ServiceAddress.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for addr in context['addresses']:
            addr.active_incidents = Incident.objects.filter(
                affected_addresses=addr,
                is_resolved=False
            )
        return context
