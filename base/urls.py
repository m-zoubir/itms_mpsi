# -*- coding: utf-8 -*-
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'demandes', views.DemandeViewSet)
router.register(r'interventions', views.InterventionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('', views.getComponents ,name='get-components'),
]
