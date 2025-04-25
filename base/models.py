from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    designation = models.TextField()

    def __str__(self):
        return self.designation

class Composant(models.Model):
    TYPE_CHOICES = [
        ('Nouveau', 'Nouveau'),
        ('Ancien', 'Ancien'),
    ]
    
    STATUS_CHOICES = [
        ('Used', 'Used'),
        ('Free', 'Free'),
    ]

    id_composant = models.AutoField(primary_key=True)
    type_composant = models.CharField(max_length=20, choices=TYPE_CHOICES)
    model_reference = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100)
    designation = models.TextField()
    observation = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    
    numero_serie_eq_source = models.CharField(max_length=100, blank=True, null=True)
    numero_inventaire_eq_source = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    
    quantity = models.IntegerField(blank=True, null=True )
    disponible = models.BooleanField(default=True , blank=True, null=True)

    def __str__(self):
        return f"{self.type_composant} - {self.designation}"

    def clean(self):
        if self.type_composant == 'Ancien':
            if not self.numero_serie_eq_source:
                raise ValidationError({'numero_serie_eq_source': 'Required for Ancien composant'})
            if not self.numero_inventaire_eq_source:
                raise ValidationError({'numero_inventaire_eq_source': 'Required for Ancien composant'})
            if not self.status:
                raise ValidationError({'status': 'Required for Ancien composant'})
            
            self.quantity = None
            self.disponible = None
            
        elif self.type_composant == 'Nouveau':
            if self.quantity is None:
                raise ValidationError({'quantity': 'Required for Nouveau composant'})
            if self.disponible is None:
                raise ValidationError({'disponible': 'Required for Nouveau composant'})
            
            self.numero_serie_eq_source = None
            self.numero_inventaire_eq_source = None
            self.status = None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)





class Equipement(models.Model):


    id_equipement = models.AutoField(primary_key=True)
    model_reference = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100)
    designation = models.TextField()
    observation = models.TextField(blank=True, null=True)
    numero_inventaire= models.CharField(max_length=100)
    

    def __str__(self):
        return self.designation

    



#--------------------------------------Users------------------------------------



class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    pass