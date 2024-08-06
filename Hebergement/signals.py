from django.db.models.signals import post_migrate
from django.dispatch import receiver

from Hebergement.models import *

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TypeAccessoire, AccessoireHebergement


@receiver(post_migrate)
def create_initial_types(sender, **kwargs):
    if sender.name == "Hebergement":
        type_accessoire_hebergement = [
            "Security",
            "Restauration",
            "High-tech",
            "Welcome",
            "Room service",
            "General",
        ]

        for _type_acc in type_accessoire_hebergement:
            TypeAccessoire.objects.get_or_create(nom_type=_type_acc)

        # Créer les accessoires
        accessoires_hotel = [
            ("Piscine", "General"),
            ("Spa", "General"),
            ("Salle de sport", "General"),
            ("Bar", "Restauration"),
            ("Restaurant", "Restauration"),
            ("Parking", "General"),
            ("Service de conciergerie", "General"),
            ("Centre d'affaires", "General"),
            ("Sauna", "General"),
            ("Wi-Fi gratuit", "High-tech"),
            ("Télévision", "High-tech"),
            ("Climatisation", "High-tech"),
            ("Chargers", "High-tech"),
            ("Service de chambre", "Room service"),
            ("Petit-déjeuner en chambre", "Room service"),
            ("Menu personnalisé", "Room service"),
            ("Repas à la carte", "Room service"),
            ("Sécurité 24h/24", "Security"),
            ("Détecteur de fumée", "Security"),
            ("Coffre-fort", "Security"),
            ("Surveillance vidéo", "Security"),
            ("Accueil VIP", "Welcome"),
            ("Fleurs de bienvenue", "Welcome"),
            ("Panier de fruits", "Welcome"),
            ("Service de navette", "Welcome"),
            ("Service de réservation", "Welcome"),
            ("Parking gratuit", "General"),
            ("Wi-Fi haute vitesse", "High-tech"),
            ("Jeux vidéo", "High-tech"),
            ("Équipements sportifs", "General"),
        ]

        for nom, type_nom in accessoires_hotel:
            type_accessoire = TypeAccessoire.objects.get(nom_type=type_nom)
            AccessoireHebergement.objects.get_or_create(
                nom_accessoire=nom, type_accessoire=type_accessoire
            )

        hebergement_types = [
            "Hotel",
            "Bungallow",
            "Appartement",
            "Maison d'hôtes",
            "Chalet",
            "Gîte",
            "Camping",
            "Auberge de jeunesse",
            "Villa",
            "Motel",
            "Pension",
            "Resort",
            "Chambre d'hôtes",
            "Cottage",
            "Lodge",
            "Hostel",
            "Riad",
            "Ryokan",
            "Cabane",
            "Bateau",
            "Tente",
        ]

        for type_name in hebergement_types:
            TypeHebergement.objects.get_or_create(type_name=type_name)

        accessoires_chambre = [
            "Wifi",
            "Bureau",
            "Coffre-fort",
            "Table à manger",
            "Télévision à écran plat",
            "Accès au salon exécutif",
            "Service de réveil",
            "Service de réveil / réveil",
            "Canapé",
            "Ventilateur",
            "Serviettes",
            "Télévision",
            "Linge de maison",
            "Sol carrelé / en marbre",
            "Chauffage",
            "Téléphone",
            "Dressing",
            "Chaînes du câble",
            "Armoire ou penderie",
            "Chaînes satellite",
            "Climatisation",
            "Coin repas",
        ]

        for i in accessoires_chambre:
            AccessoireChambre.objects.get_or_create(nom_accessoire=i)

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
                type_chambre=_type[0],
                nombre_min_personnes=_type[1],
                nombre_max_personnes=_type[2],
            )
