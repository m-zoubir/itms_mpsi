from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import *

@receiver(m2m_changed, sender=Intervention.composants_utilises.through)
def update_composants_on_intervention(sender, instance, action, reverse, pk_set, **kwargs):
    if action == 'post_add':
        for composant_id in pk_set:
            composant = Composant.objects.get(pk=composant_id)
            if composant.type_composant == 'Ancien':
                composant.status = 'Used'
                composant.save()
            elif composant.type_composant == 'Nouveau':
                if composant.quantity and composant.quantity > 0:
                    composant.quantity -= 1
                    if composant.quantity == 0:
                        composant.disponible = False
                    composant.save()
