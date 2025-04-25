from rest_framework import serializers
from .models import Demande, Intervention, Component

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class InterventionSerializer(serializers.ModelSerializer):
    components_used = ComponentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Intervention
        fields = '__all__'
        read_only_fields = ('date_sortie',)

class DemandeSerializer(serializers.ModelSerializer):
    interventions = InterventionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Demande
        fields = '__all__'
        read_only_fields = ('date_depot',)