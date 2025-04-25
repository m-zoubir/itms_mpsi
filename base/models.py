from django.db import models
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Demande(models.Model):
    TYPE_MATERIEL_CHOICES = [
        ('Ordinateur', 'Ordinateur'),
        ('Imprimante', 'Imprimante'),
        ('Serveur', 'Serveur'),
        ('Autre', 'Autre'),
    ]
    
    STATUS_DEMANDE_CHOICES = [
        ('Nouvelle', 'Nouvelle'),
        ('Acceptee', 'Acceptée'),
        ('Rejetee', 'Rejetée'),
    ]
    
    TYPE_DEPOSANT_CHOICES = [
        ('Etudiant', 'Étudiant'),
        ('Ensiegnant', 'Enseignant'),
        ('Employer', 'Employé'),
    ]

    type_materiel = models.CharField(max_length=100, choices=TYPE_MATERIEL_CHOICES)
    marque = models.CharField(max_length=100)
    numero_inventaire = models.CharField(max_length=100)
    service_affectation = models.CharField(max_length=100)
    date_depot = models.DateTimeField(auto_now_add=True)
    nom_deposant = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100, choices=TYPE_DEPOSANT_CHOICES)
    panne_declaree = models.TextField()
    status_demande = models.CharField(max_length=100, choices=STATUS_DEMANDE_CHOICES, default='Nouvelle')


    def __str__(self):
        return f"Demande #{self.id} - {self.type_materiel}"


class Intervention(models.Model):
    PRIORITE_CHOICES = [
        ('Haute', 'Haute'),
        ('Moyenne', 'Moyenne'),
        ('Basse', 'Basse'),
    ]
    
    STATUS_INTERVENTION_CHOICES = [
        ('enCours', 'En Cours'),
        ('Termine', 'Terminé'),
    ]

    demande_id = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='interventions')
    technicien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interventions')
    numero_serie = models.CharField(max_length=100)
    priorite = models.CharField(max_length=100, choices=PRIORITE_CHOICES)
    panne_trouvee = models.TextField()
    composants_utilises = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_INTERVENTION_CHOICES, default='enCours')
    date_sortie = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Intervention #{self.id} - Demande #{self.demande.id}"

    def save(self, *args, **kwargs):
        if self.status == 'Termine' and not self.date_sortie:
            from django.utils import timezone
            self.date_sortie = timezone.now()
        super().save(*args, **kwargs)