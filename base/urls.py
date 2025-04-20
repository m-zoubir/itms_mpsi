from django.urls import path
from . import views
from .views import LoginView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Route pour la connexion
    path('', views.getComponents, name='get-components'),  # Route pour les composants
    path('signup/', SignupView.as_view(), name='signup'),
]
