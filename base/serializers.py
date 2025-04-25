from rest_framework import serializers
from .models import Categorie, Composant , Equipement

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
