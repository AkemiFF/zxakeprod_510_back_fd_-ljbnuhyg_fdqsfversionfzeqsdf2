from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_migrate
from django.dispatch import receiver


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

    types_transport = [
        "Autocar",
        "Minibus",
        "Voiture de luxe",
        "Train",
        "Avion",
        "Bateau",
        "Vélo",
        "Scooter",
        "Marche",
        "Taxi",
        "Motocyclette",
        "Ferry",
        "Caleche",
        "Tramway",
        "Téléphérique",
    ]

    for type_transport in types_transport:
        TypeTransport.objects.get_or_create(nom_type=type_transport)
