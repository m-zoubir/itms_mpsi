from rest_framework import serializers
from .models import Demande, Intervention
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class DemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = '__all__'
        read_only_fields = ['date_depot']

class InterventionSerializer(serializers.ModelSerializer):
    technicien_details = UserSerializer(source='technicien', read_only=True)
    demande_details = DemandeSerializer(source='demande', read_only=True)

    class Meta:
        model = Intervention
        fields = '__all__'
        read_only_fields = ['date_sortie']

    def validate(self, data):
        if self.instance and self.instance.status == 'Termine' and data.get('status') != 'Termine':
            raise serializers.ValidationError("Cannot change status from Terminé to another status.")
        return data