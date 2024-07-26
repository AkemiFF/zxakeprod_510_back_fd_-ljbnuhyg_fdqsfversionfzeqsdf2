from django.apps import AppConfig


class ArtisanalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Artisanal"

    def ready(self):
        import Artisanal.signals
