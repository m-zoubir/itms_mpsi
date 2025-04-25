from django.urls import path
from . import views

urlpatterns = [
    path('demandes/', views.DemandeListView.as_view(), name='demande_list'),
    path('demandes/<int:pk>/', views.DemandeDetailView.as_view(), name='demande_detail'),
    path('interventions/', views.InterventionListView.as_view(), name='intervention_list'),
    path('interventions/<int:pk>/', views.InterventionDetailView.as_view(), name='intervention_detail'),
]
