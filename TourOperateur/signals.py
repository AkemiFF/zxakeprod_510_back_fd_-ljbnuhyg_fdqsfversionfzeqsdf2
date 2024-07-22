from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import *


@receiver(post_migrate)
def create_initial_types(sender, **kwargs):
    inclusions_voyage = [
        "Transport",
        "Hébergement",
        "Restauration",
        "Activités",
        "Assurance",
        "Guide touristique",
        "Wifi",
        "Parking",
        "Navette",
        "Climatisation",
        "Bain à remous",
        "Spa",
        "Piscine",
        "Salle de sport",
        "Bar",
        "Centre d'affaires",
        "Service de blanchisserie",
        "Animaux acceptés",
        "Accès handicapé",
        "Transfert aéroport",
        "Petit-déjeuner",
        "Déjeuner",
        "Dîner",
        "Guide local",
        "Excursions",
        "Billets d'entrée",
        "Assistance 24/7",
    ]

    for inclusion in inclusions_voyage:
        TypeInclusion.objects.get_or_create(nom_inclusion=inclusion)
