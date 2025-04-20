import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignupSerializer
from django.utils.timezone import now

# Create your views here.


def getComponents(request):
    return render(request,'componentsListPage.html')

def createComponent(request):
    return render(request )

def updateComponent(request , pk):
    return render(request)



logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        logger.debug("Login attempt received.")  # Log d'une tentative de connexion

        # Utilisation du sérialiseur
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug("Serializer is valid. Authenticating user...")

            user = serializer.validated_data
            logger.debug(f"User authenticated: {user.email}")  # Log de l'email de l'utilisateur
            
            # Enregistrer l'heure de la dernière connexion
            user.last_login = now()
            user.save()

            logger.debug("User last_login updated.")  # Log de la mise à jour

            return Response({"message": "Login successful", "user_id": user.id})

        logger.error(f"Invalid credentials: {serializer.errors}")  # Log des erreurs en cas d'échec
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)