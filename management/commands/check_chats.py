from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Wakhtane.models import Chat


class Command(BaseCommand):
    help = 'Vérifie et corrige les données de discussions'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()

        for user in users:
            chats_created = Chat.objects.filter(created_by=user)
            chats_participated = Chat.objects.filter(participants=user)

            self.stdout.write(f'Utilisateur : {user}')
            self.stdout.write(f'  Discussions créées : {list(chats_created)}')
            self.stdout.write(f'  Discussions participées : {list(chats_participated)}')
