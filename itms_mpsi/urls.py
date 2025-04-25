
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import *





router = DefaultRouter()
router.register(r'api/categories', CategorieViewSet, basename='categories')
router.register(r'api/composants', ComposantViewSet, basename='composants')
router.register(r'api/equipements', EquipementViewSet, basename='equipements')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    ]