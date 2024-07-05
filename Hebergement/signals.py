from django.db.models.signals import post_migrate
from django.dispatch import receiver

from Hebergement.models import *


@receiver(post_migrate)
def create_initial_types(sender, **kwargs):
    hebergement_types = [
        "Hotel", "Bungallow", "Appartement", "Maison d'hôtes", "Chalet",
        "Gîte", "Camping", "Auberge de jeunesse", "Villa", "Motel",
        "Pension", "Resort", "Chambre d'hôtes", "Cottage", "Lodge",
        "Hostel", "Riad", "Ryokan", "Cabane", "Bateau", "Tente"
    ]

    for type_name in hebergement_types:
        TypeHebergement.objects.get_or_create(type_name=type_name)

    accessoires_chambre = [
        "Wifi", "Bureau", "Coffre-fort", "Table à manger",
        "Télévision à écran plat", "Accès au salon exécutif",
        "Service de réveil", "Service de réveil / réveil",
        "Canapé", "Ventilateur", "Serviettes", "Télévision",
        "Linge de maison", "Sol carrelé / en marbre",
        "Chauffage", "Téléphone", "Dressing",
        "Chaînes du câble", "Armoire ou penderie",
        "Chaînes satellite", "Climatisation", "Coin repas"
    ]

    for i in accessoires_chambre:
        AccessoireChambre.objects.get_or_create(nom_accessoire=i)

    accessoires_hotel = [
        "Piscine", "Spa", "Salle de sport", "Bar", "Restaurant",
        "Salle de conférence", "Service de blanchisserie",
        "Navette aéroport", "Parking", "Service de conciergerie",
        "Centre d'affaires", "Sauna", "Wi-Fi gratuit",
        "Service de chambre", "Réception 24h/24"
    ]

    for nom in accessoires_hotel:
        AccessoireHebergement.objects.get_or_create(nom_accessoire=nom)

    type_de_chambres = [
        ("Standard", 1, 2),
        ("Supérieur/Delux", 1, 2),
        ("Suite", 2, 4),
        ("Familiale", 3, 4),
        ("Communicante", 4, 6),
        ("Avec vue", 1, 2),
    ]
    for _type in type_de_chambres:
        Chambre.objects.get_or_create(
            type_chambre=_type[0], nombre_min_personnes=_type[1], nombre_max_personnes=_type[2])
