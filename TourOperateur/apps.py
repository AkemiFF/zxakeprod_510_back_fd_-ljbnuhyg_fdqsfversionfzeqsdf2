from django.apps import AppConfig


class TouroperateurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "TourOperateur"

    def ready(self):
        import TourOperateur.signals  # type: ignore
