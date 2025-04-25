from django.contrib import admin

# Register your models here.
from .models import Composant , Categorie, Equipement , User

admin.site.register(Composant)
admin.site.register(Categorie)
admin.site.register(Equipement)
admin.site.register(User)
