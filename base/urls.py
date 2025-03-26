from django.urls import path
from . import views

urlpatterns = [
    path('', views.getComponents ,name='get-components'),
]
