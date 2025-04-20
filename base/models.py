from django.db import models


class Component(models.Model):
    numero_serie = models.CharField(max_length=200)
    numero_serie_eq = models.CharField(max_length=200)
    numero_inventaire_eq = models.CharField(max_length=200)
    designation = models.TextField()
    observation = models.TextField(null=True, blank=True)
    model_reference = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.designation
