from Accounts.models import ResponsableEtablissement
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from Accounts.models import *
from django.contrib.auth.models import User
from django.utils import timezone


class TypeHebergement(models.Model):
    type_name = models.CharField(
        max_length=50, unique=True, null=True, blank=True,
    )

    def __str__(self):
        return self.type_name


class HebergementImage(models.Model):
    hebergement = models.ForeignKey(
        'Hebergement', on_delete=models.CASCADE, related_name='images')
    couverture = models.BooleanField(default=False)
    legende_hebergement = models.CharField(max_length=200, blank=True)
    images = models.ImageField(
        upload_to='images/images_Hebergement', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.images.name


class AccessoireHebergement(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_accessoire


class Chambre(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_min_personnes = models.IntegerField(default=1)
    nombre_max_personnes = models.IntegerField(default=1)

    def __str__(self):
        return self.type_chambre


class ChambrePersonaliser(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_personnes = models.IntegerField(default=1)

    def __str__(self):
        return self.type_chambre


class Hebergement(models.Model):
    nom_hebergement = models.CharField(max_length=100)
    description_hebergement = models.TextField()
    nombre_etoile_hebergement = models.IntegerField()
    responsable_hebergement = models.ForeignKey(
        ResponsableEtablissement, on_delete=models.CASCADE, related_name='hebergements')
    type_hebergement = models.ForeignKey(
        TypeHebergement, null=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_hebergement


class HebergementChambre(models.Model):
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE)
    chambre = models.ForeignKey(
        Chambre, on_delete=models.CASCADE, null=True, blank=True)
    chambre_personaliser = models.ForeignKey(
        ChambrePersonaliser, on_delete=models.CASCADE, null=True, blank=True)
    prix_nuit_chambre = models.DecimalField(max_digits=8, decimal_places=2)
    disponible_chambre = models.IntegerField(null=True)
    accessoires = models.ManyToManyField(
        'AccessoireChambre', through='HebergementChambreAccessoire')

    def __str__(self):
        return f'{self.hebergement} - {self.chambre} - {self.chambre_personaliser}'

class Localisation(models.Model):
    adresse = models.CharField(max_length=200, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    hebergement_id = models.OneToOneField(
        Hebergement, on_delete=models.CASCADE, related_name='hebergement', null=True, blank=True)

    def __str__(self):
        return self.adresse


class HebergementAccessoire(models.Model):
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE)
    accessoire = models.ForeignKey(
        AccessoireHebergement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hebergement.nom_hebergement} - {self.accessoire.nom_accessoire}"


class AccessoireChambre(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_accessoire



class HebergementChambreAccessoire(models.Model):
    hebergement_chambre = models.ForeignKey(
        HebergementChambre, on_delete=models.CASCADE)
    accessoire_chambre = models.ForeignKey(
        AccessoireChambre, on_delete=models.CASCADE)

    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.hebergement_chambre} - {self.accessoire_chambre}'


class ImageChambre(models.Model):
    hebergement_chambre = models.ForeignKey(
        'HebergementChambre', on_delete=models.CASCADE, related_name='images_chambre')
    images = models.ImageField(upload_to='images/images_chambre')
    couverture = models.BooleanField(default=False)
    legende_chambre = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.images.name

# Reservation


class Reservation(models.Model):
    hotel_reserve = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name='reservations')
    chambre_reserve = models.ForeignKey(
        HebergementChambre, on_delete=models.CASCADE, related_name='reservations')
    client_reserve = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='reservations')
    date_debut_reserve = models.DateField()
    date_fin_reserve = models.DateField()
    nombre_personnes_reserve = models.IntegerField(
        default=1)
    prix_total_reserve = models.DecimalField(max_digits=10, decimal_places=2)
    est_validee_reserve = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AvisClients(models.Model):
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name='avis_hotel')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='avis_client')
    commentaire = models.CharField(null=True, max_length=500)
    note = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Note: {self.note} - Hebergement: {self.hebergement.nom_hebergement}"
