from rest_framework import viewsets
from .models import Categorie, Composant , Equipement , User , Demande , Intervention
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status ,permissions , generics
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models.functions import ExtractMonth
from django.db.models import Count


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.AllowAny]  


class ComposantViewSet(viewsets.ModelViewSet):
    queryset = Composant.objects.all()
    serializer_class = ComposantSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    
class   EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [permissions.AllowAny]  


#-------------------Users----------------------

class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    permission_classes = [permissions.IsAdminUser] 
    
    def perform_create(self, serializer):
        user = serializer.save()
        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)




class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user_id': user.id,
            'email': user.email,
            'is_admin': user.is_staff,  
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out"}, 
                          status=status.HTTP_200_OK)
        
        return response



class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

class AdminPasswordUpdateView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': 'Password updated successfully'})
    

#------------------Interventions et Demandes--------------------------


class DemandeViewSet(viewsets.ModelViewSet):
    queryset = Demande.objects.all()
    serializer_class = DemandeSerializer
    permission_classes = [permissions.AllowAny]  

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    permission_classes = [permissions.AllowAny]  



#------------------Dashboard--------------------------

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.timezone import now

class DashboardAPIView(APIView):
    def get(self, request):
        current_date = now()
        current_month = current_date.month
        current_year = current_date.year
        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1

        # --- Helper Function ---
        def percentage_diff(current, last):
            return 100 if last == 0 and current > 0 else round(((current - last) / last) * 100) if last > 0 else 0

        # --- Monthly Counts ---
        demandes_this_month = Demande.objects.filter(date_depot__year=current_year, date_depot__month=current_month).count()
        demandes_last_month = Demande.objects.filter(date_depot__year=last_month_year, date_depot__month=last_month).count()
        demandes_this_year = Demande.objects.filter(date_depot__year=current_year).count()

        interventions_this_month = Intervention.objects.filter(created_at__year=current_year, created_at__month=current_month, status="enCours").count()
        interventions_last_month = Intervention.objects.filter(created_at__year=last_month_year, created_at__month=last_month, status="enCours").count()
        interventions_this_year = Intervention.objects.filter(created_at__year=current_year).count()

        composants_ancien_this_month = Composant.objects.filter(created_at__year=current_year, created_at__month=current_month, status='Free', type_composant='Ancien').count()
        composants_ancien_last_month = Composant.objects.filter(created_at__year=last_month_year, created_at__month=last_month, status='Free', type_composant='Ancien').count()
        composants_this_year = Composant.objects.filter(created_at__year=current_year).count()

        composants_nouveau_this_month = Composant.objects.filter(created_at__year=current_year, created_at__month=current_month, disponible=True, type_composant='Nouveau').count()
        composants_nouveau_last_month = Composant.objects.filter(created_at__year=last_month_year, created_at__month=last_month, disponible=True, type_composant='Nouveau').count()

        equipements_this_month = Equipement.objects.filter(created_at__year=current_year, created_at__month=current_month).count()
        equipements_last_month = Equipement.objects.filter(created_at__year=last_month_year, created_at__month=last_month).count()
        equipements_this_year = Equipement.objects.filter(created_at__year=current_year).count()

        # --- Monthly demandes by month ---
        demandes_by_month = Demande.objects.filter(date_depot__year=current_year).annotate(
            month=ExtractMonth('date_depot')
        ).values('month').annotate(value=Count('id')).order_by('month')

        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }

        demandes_months = [{
            "month": month_names.get(item["month"], "Unknown"),
            "value": item["value"]
        } for item in demandes_by_month]

        # --- Yearly stats for each entity ---
        def yearly_stats(model, date_field):
            return model.objects.annotate(year=ExtractYear(date_field)).values("year").annotate(total=Count("id")).order_by("year")

        data = {
            "totals": [
                {
                    "name": "Total des demandes",
                    "value": Demande.objects.count(),
                    "pourcentage diff": percentage_diff(demandes_this_month, demandes_last_month)
                },
                {
                    "name": "Interventions actives",
                    "value": interventions_this_month,
                    "pourcentage diff": percentage_diff(interventions_this_month, interventions_last_month)
                },
                {
                    "name": "Anciens composants disponibles",
                    "value": Composant.objects.filter(status='Free', type_composant='Ancien').count(),
                    "pourcentage diff": percentage_diff(composants_ancien_this_month, composants_ancien_last_month)
                },
                {
                    "name": "Nouveaux composants disponibles",
                    "value": Composant.objects.filter(disponible=True, type_composant='Nouveau').count(),
                    "pourcentage diff": percentage_diff(composants_nouveau_this_month, composants_nouveau_last_month)
                },
                {
                    "name": "Équipements total",
                    "value": Equipement.objects.count(),
                    "pourcentage diff": percentage_diff(equipements_this_month, equipements_last_month)
                },
            ],
            "demandes": [
                {
                    "year": current_year,
                    "months": demandes_months
                }
            ],
            "demandestats": 
                {
                    "year": current_year,
                    "total": demandes_this_year,
                    "total rejetee": Demande.objects.filter(status_demande='Rejetee', date_depot__year=current_year).count(),
                    "total acceptee": Demande.objects.filter(status_demande='Acceptee', date_depot__year=current_year).count(),
                    "demande_years": list(yearly_stats(Demande, "date_depot")),

                },
            
            "interventionsstats": 
                {
                    "year": current_year,
                    "total": interventions_this_year,
                    "total irreparable": Intervention.objects.filter(status='Irreparable', created_at__year=current_year).count(),
                    "total completed": Intervention.objects.filter(status='Termine', created_at__year=current_year).count(),
                    "total encours": Intervention.objects.filter(status='enCours', created_at__year=current_year).count(),
                    "intervention_years": list(yearly_stats(Intervention, "created_at")),

                },
            
            "composantstats": 
                {
                    "year": current_year,
                    "total": composants_this_year,
                    "total ancien": Composant.objects.filter(type_composant='Ancien', created_at__year=current_year).count(),
                    "total nouveau": Composant.objects.filter(type_composant='Nouveau', created_at__year=current_year).count(),
                    "composant_years": list(yearly_stats(Composant, "created_at")),

                }
           
           ,
            "equipementstats": list(yearly_stats(Equipement, "created_at")),
        }

        return Response(data)
