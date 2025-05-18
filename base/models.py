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

    type_composant = models.CharField(max_length=20, choices=TYPE_CHOICES)
    model_reference = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100)
    designation = models.TextField()
    observation = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    numero_serie_eq_source = models.CharField(max_length=100, blank=True, null=True)
    numero_inventaire_eq_source = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        default='Free'
    )

    quantity = models.IntegerField(blank=True, null=True, default=1)
    disponible = models.BooleanField(default=True, blank=True, null=True)

    image = models.ImageField(upload_to='images_composants/', blank=True, null=True)


    def __str__(self):
        return f"{self.type_composant} - {self.designation}"

   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)





class Equipement(models.Model):


    model_reference = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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




#--------------------------------------Interventions et Demandes------------------------------------



class Demande(models.Model):
    TYPE_MATERIEL_CHOICES = [
        ('Ordinateur', 'Ordinateur'),
        ('Imprimante', 'Imprimante'),
        ('Serveur', 'Serveur'),
        ('Autre', 'Autre'),
    ]
    
    STATUS_DEMANDE_CHOICES = [
        ('Nouvelle', 'Nouvelle'),
        ('Acceptee', 'Acceptee'),
        ('Rejetee', 'Rejetée'),
    ]
    
    TYPE_DEPOSANT_CHOICES = [
        ('Etudiant', 'Etudiant'),
        ('Enseignant', 'Enseignant'),
        ('Employe', 'Employe'),
    ]

    type_materiel = models.CharField(max_length=100, choices=TYPE_MATERIEL_CHOICES)
    marque = models.CharField(max_length=100, blank=True, null=True)
    numero_inventaire = models.CharField(max_length=100 , blank=True, null=True)
    service_affectation = models.CharField(max_length=100)
    date_depot = models.DateTimeField(auto_now_add=True)
    nom_deposant = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100, choices=TYPE_DEPOSANT_CHOICES)
    panne_declaree = models.TextField(blank=True, null=True)
    status_demande = models.CharField(max_length=100, choices=STATUS_DEMANDE_CHOICES, default='Nouvelle')


    def __str__(self):
        return f"Demande #{self.id} - {self.type_materiel}"
    

    @property
    def designation(self):
        return f"{self.type_materiel} - {self.marque or 'Sans marque'}"




class Intervention(models.Model):
    PRIORITE_CHOICES = [
        ('Haute', 'Haute'),
        ('Moyenne', 'Moyenne'),
        ('Basse', 'Basse'),
    ]
    
    STATUS_INTERVENTION_CHOICES = [
        ('enCours', 'enCours'),
        ('Termine', 'Termine'),
        ('Irreparable', 'Irreparable'),
    ]


    demande_id = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='interventions')
    created_at = models.DateTimeField(auto_now_add=True)
    technicien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interventions')
    numero_serie = models.CharField(max_length=100 , blank=True, null=True)
    priorite = models.CharField(max_length=100, choices=PRIORITE_CHOICES, default='Moyenne')
    panne_trouvee = models.TextField(blank=True, null=True)
    composants_utilises = models.ManyToManyField(
        Composant,
        blank=True,
    )    

    status = models.CharField(max_length=100, choices=STATUS_INTERVENTION_CHOICES, default='enCours')
    date_sortie = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Intervention #{self.id} - Demande #{self.demande_id}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
                    
        if self.status == 'Termine' and not self.date_sortie:
            from django.utils import timezone
            self.date_sortie = timezone.now()
            super().save(*args, **kwargs)

    
    @property
    def designation(self):
        demande = self.demande_id
        return f"{demande.type_materiel} - {demande.marque or 'Sans marque'}"
    
    @property
    def numero_inventaire(self):
        demande = self.demande_id
        return demande.numero_inventaire










""" if self.composants_utilises.exists():
            for composant in self.composants_utilises.all():
                if composant.type_composant == 'Ancien':
                    composant.status = 'Used'
                    composant.save()
                elif composant.type_composant == 'Nouveau':
                    if composant.quantity > 0:
                        composant.quantity -= 1
                        if composant.quantity == 0:
                            composant.disponible = False
                        composant.save()
        """