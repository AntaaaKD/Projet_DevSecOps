# Dans votre application Django, par exemple 'Wakhtane'
# wakhtane/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages  # Importez si vous souhaitez utiliser les messages Django

from .models import VideoCall  # Assurez-vous d'importer votre modèle VideoCall

@receiver(post_save, sender=VideoCall)
def notify_participants_on_create(sender, instance, created, **kwargs):
    if created:
        participants = instance.participants.all()
        for participant in participants:
            # Exemple d'utilisation des messages Django
            message_text = f"Un nouvel appel vidéo intitulé '{instance.title}' a été créé."
            messages.info(participant, message_text)
