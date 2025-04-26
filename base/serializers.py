from rest_framework import serializers
from .models import Categorie, Composant , Equipement , User , Demande , Intervention
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = ['id_categorie', 'designation']

class ComposantSerializer(serializers.ModelSerializer):
    categorie_details = CategorieSerializer(source='categorie', read_only=True)
    
    categorie = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Composant
        fields = [
            'id_composant', 'type_composant', 'model_reference', 'numero_serie',
            'designation', 'observation', 'categorie' ,'categorie_details',
            'numero_serie_eq_source', 'numero_inventaire_eq_source', 'status',
            'quantity', 'disponible'
        ]
        extra_kwargs = {
            'disponible': {'default': True},
            'quantity': {'default': 1},
            'status': {'default': 'Free'}
        }

    def validate(self, data):
        type_composant = data.get('type_composant', self.instance.type_composant if self.instance else None)
        
        if type_composant == 'Ancien':
            required_fields = {
                'numero_serie_eq_source': 'Required for Ancien composant',
                'numero_inventaire_eq_source': 'Required for Ancien composant',
                'status': 'Required for Ancien composant'
            }
            for field, error_msg in required_fields.items():
                if not data.get(field):
                    raise serializers.ValidationError({field: error_msg})
            
            data['quantity'] = None
            data['disponible'] = None
            
        elif type_composant == 'Nouveau':
            if data.get('quantity') is None:
                data['quantity'] = 1
            if data.get('disponible') is None:
                data['disponible'] = True
                
            data['numero_serie_eq_source'] = None
            data['numero_inventaire_eq_source'] = None
            data['status'] = None
        
        return data
    


class EquipementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipement
        fields = '__all__'




#----------------------Users-----------------------------

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'email']

class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
            )
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user
    

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)




#-----------------------Interventions et Demandes------------------------------


class InterventionSerializer(serializers.ModelSerializer):
    components_used = ComposantSerializer(many=True, read_only=True)
    
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