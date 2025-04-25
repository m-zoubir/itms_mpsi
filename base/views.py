from django.views.generic import ListView, DetailView
from .models import Demande, Intervention

class DemandeListView(ListView):
    model = Demande
    template_name = 'demandes/list.html'
    context_object_name = 'demandes'

class DemandeDetailView(DetailView):
    model = Demande
    template_name = 'demandes/detail.html'
    context_object_name = 'demande'

class InterventionListView(ListView):
    model = Intervention
    template_name = 'interventions/list.html'
    context_object_name = 'interventions'

class InterventionDetailView(DetailView):
    model = Intervention
    template_name = 'interventions/detail.html'
    context_object_name = 'intervention'
