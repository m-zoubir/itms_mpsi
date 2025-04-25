from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Demande, Intervention
from .serializers import DemandeSerializer, InterventionSerializer
from django_filters.rest_framework import DjangoFilterBackend

class DemandeViewSet(viewsets.ModelViewSet):
    queryset = Demande.objects.all().order_by('-date_depot')
    serializer_class = DemandeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type_materiel', 'status_demande', 'type_deposant']
    search_fields = ['nom_deposant', 'numero_inventaire', 'marque']
    ordering_fields = ['date_depot', 'status_demande']

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all().select_related('demande', 'technicien')
    serializer_class = InterventionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priorite', 'demande__status_demande']
    search_fields = ['numero_serie', 'demande__nom_deposant']
    ordering_fields = ['date_sortie', 'priorite']

    def perform_create(self, serializer):
        serializer.save(technicien=self.request.user)


def getComponents(request):
    return render(request,'componentsListPage.html')

def createComponent(request):
    return render(request )

def updateComponent(request , pk):
    return render(request)

