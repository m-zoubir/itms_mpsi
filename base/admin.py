from django.contrib import admin
from .models import Demande, Intervention

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_materiel', 'nom_deposant', 'status_demande', 'date_depot')
    list_filter = ('type_materiel', 'status_demande')
    search_fields = ('nom_deposant', 'numero_inventaire', 'email')

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'demande_id', 'technicien', 'priorite', 'status', 'date_sortie')
    list_filter = ('status', 'priorite')
    search_fields = ('demande_id__id', 'technicien__username', 'numero_serie')
