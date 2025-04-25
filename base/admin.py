# -*- coding: utf-8 -*-
from .models import Component
from django.contrib import admin
from .models import Demande, Intervention

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_materiel', 'nom_deposant', 'status_demande', 'date_depot')
    list_filter = ('status_demande', 'type_deposant', 'type_materiel')
    search_fields = ('nom_deposant', 'numero_inventaire', 'marque')
    date_hierarchy = 'date_depot'

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'demande', 'technicien', 'status', 'priorite', 'date_sortie')
    list_filter = ('status', 'priorite')
    search_fields = ('numero_serie', 'demande__nom_deposant')
    raw_id_fields = ('demande', 'technicien')
    date_hierarchy = 'date_sortie'



admin.site.register(Component)