# Dans votre fichier d'application Django, par exemple 'Wakhtane/apps.py'

from django.apps import AppConfig

class WakhtaneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Wakhtane'

    def ready(self):
        import Wakhtane.signals  # Assurez-vous d'importer votre fichier signals.py ici
