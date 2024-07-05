from django.apps import AppConfig


class AdministrateursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Hebergement'

    def ready(self):
        import Hebergement.signals
