from rest_framework import viewsets
from .models import Categorie, Composant , Equipement
from .serializers import CategorieSerializer, ComposantSerializer , EquipementSerializer
from rest_framework.response import Response



class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ComposantViewSet(viewsets.ModelViewSet):
    queryset = Composant.objects.all()
    serializer_class = ComposantSerializer
    
class   EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer