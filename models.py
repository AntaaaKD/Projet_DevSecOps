from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from TEST import settings
from accounts.models import CustomUser


# Chat Model
class Contact(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')


    def __str__(self):
        return self.user.email

class Chat(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_created')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats_participated')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def recipient_email(self):
        # Retourne l'email du premier participant autre que l'utilisateur créateur
        for participant in self.participants.all():
            if participant != self.created_by:
                return participant.email
        return None

# Message Model

# Group Model
class GroupDiscussion(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, related_name='group_discussions_created', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_members', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Définition du signal post-save pour GroupDiscussion
@receiver(post_save, sender=GroupDiscussion)
def add_participants_to_discussion(sender, instance, created, **kwargs):
    if created:
        # Ajoute tous les participants comme membres de la discussion
        for participant in instance.members.all():
            instance.members.add(participant)
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)  # Permettre au champ content d'être vide
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    discussion = models.ForeignKey(GroupDiscussion, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # Ajouter le champ file

    def __str__(self):
        return f'{self.sender.email}: {self.content[:20]}'

# Video Call Model
class VideoCall(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_calls')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='video_call_participants')
    scheduled_at = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return self.title




