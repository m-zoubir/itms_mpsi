from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Utilise 'email' au lieu de 'username'
    password = serializers.CharField()

    def validate(self, data):
        # Authentifie avec l'email au lieu du nom d'utilisateur
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user
    
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Utilise le modèle utilisateur personnalisé
        fields = ['email', 'username', 'password', 'password_confirm']
        
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        # Supprimer le champ `password_confirm` car il n'est pas nécessaire pour la création
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user