from rest_framework import serializers
from .models import Categorie, Composant , Equipement , User , Demande , Intervention
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import os
from django.conf import settings



class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = ['id_categorie', 'designation']

class ComposantSerializer(serializers.ModelSerializer):
    categorie_details = CategorieSerializer(source='categorie', read_only=True)
    image_url = serializers.SerializerMethodField()
    categorie = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Composant
        fields = [
            'id', 'type_composant', 'model_reference', 'numero_serie',
            'designation', 'observation', 'categorie' ,'categorie_details',
            'numero_serie_eq_source', 'numero_inventaire_eq_source', 'status',
            'quantity', 'disponible', 'image' , 'created_at', 'image_url'
        ]
        
        read_only_fields = ('created_at', 'image_url')

        extra_kwargs = {
            'disponible': {'default': True},
            'quantity': {'default': 1},
            'status': {'default': 'Free'},
            'created_at': {'read_only': True},
            'image': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        type_composant = data.get('type_composant')
        
        if type_composant == 'Ancien':
            required_fields = {
                'numero_serie_eq_source': 'Required for Ancien composant',
                'numero_inventaire_eq_source': 'Required for Ancien composant',
                'status': 'Required for Ancien composant'
            }
            for field, message in required_fields.items():
                if data.get(field) in [None, '']:
                    raise serializers.ValidationError({field: message})
            
            # Ensure these are null for Ancien
            data['quantity'] = None
            data['disponible'] = None
            
        elif type_composant == 'Nouveau':
            if data.get('quantity') is None:
                data['quantity'] = 1
            if data.get('disponible') is None:
                data['disponible'] = True
                
            # Ensure these are null for Nouveau
            data['numero_serie_eq_source'] = None
            data['numero_inventaire_eq_source'] = None
            data['status'] = None
        
        return data
    

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation
    
    """
    

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
    composants_utilises = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Composant.objects.all(),
        required=False
    )
    numero_inventaire = serializers.CharField(read_only=True)

    class Meta:
        model = Intervention
        fields = '__all__'
        read_only_fields = ('date_sortie', 'numero_inventaire')

    

    def handle_composant_updates(self, composants, adding=True):
        """
        Helper method to update composant quantities and status
        adding=True when adding/using composants (quantity -1)
        adding=False when removing/unusing composants (quantity +1)
        """
        for composant in composants:
            
            if adding:
                print(f"Adding Before : {composant.quantity}")
                if composant.type_composant == 'Nouveau' and composant.disponible == True:
                    composant.quantity = max(0, (composant.quantity or 1) - 1)
                    composant.disponible = composant.quantity > 0
                else :
                    composant.status = 'Used'
                print(f"Adding After : {composant.quantity}")
            else:
                print(f"Not Adding Before : {composant.quantity}")
                if composant.type_composant == 'Nouveau':
                    composant.quantity = (composant.quantity or 0) + 1
                    composant.disponible = True
                else:
                    composant.status = 'Free'
                print(f"Not Adding After : {composant.quantity}")
            composant.save()


    def create(self, validated_data):
        composants = validated_data.pop('composants_utilises', [])
        
        intervention = Intervention.objects.create(**validated_data)
        
        if composants:
            self.handle_composant_updates(composants, adding=True)
            intervention.composants_utilises.set(composants)
        
        return intervention

    def update(self, instance, validated_data):
        old_composants = list(instance.composants_utilises.all())
        
        new_composants = validated_data.pop('composants_utilises', [])
        
        # Update the intervention instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        removed_composants = set(old_composants) - set(new_composants)
        if removed_composants:
            self.handle_composant_updates(removed_composants, adding=False)
        for removed in removed_composants:
            print(f"removed : {removed.quantity}")
        added_composants = set(new_composants) - set(old_composants)
        for added in added_composants:
            print(f"added : {added.quantity}")
        if added_composants:
            self.handle_composant_updates(added_composants, adding=True)
        
        instance.composants_utilises.set(new_composants)
        
        return instance



    

class DemandeSerializer(serializers.ModelSerializer):
    interventions = InterventionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Demande
        fields = '__all__'
        read_only_fields = ('date_depot',)




class DashboardSerializer(serializers.Serializer):
    demandes_this_month = serializers.IntegerField()
    composants_this_month = serializers.IntegerField()
    equipements_this_month = serializers.IntegerField()
    interventions_this_month = serializers.IntegerField()

    demandes_diff_rate = serializers.FloatField()
    composants_diff_rate = serializers.FloatField()
    equipements_diff_rate = serializers.FloatField()
    interventions_diff_rate = serializers.FloatField()

    demandes_by_month_year = serializers.JSONField()






class MediaFileSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    size = serializers.IntegerField()
    last_modified = serializers.DateTimeField()