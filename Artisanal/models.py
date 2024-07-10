from Accounts.models import Client
from django.conf import settings
from django.db import models
from Accounts.models import *
from django.core.exceptions import ValidationError

from Hebergement.models import Localisation


class Artisanat(models.Model):
    responsable_artisanat = models.ForeignKey(
        ResponsableEtablissement, on_delete=models.CASCADE, related_name='Aoio')
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE,)

    def __str__(self):
        return f'{self.responsable_artisanat} ({self.localisation.adresse})'


class ProduitArtisanal(models.Model):
    nom_produit_artisanal = models.CharField(max_length=100, default="")
    description_artisanat = models.TextField()
    prix_artisanat = models.DecimalField(max_digits=8, decimal_places=2)
    disponible_artisanat = models.BooleanField(default=True)
    image_artisanat = models.ImageField(
        upload_to='artisanat_images', blank=True)
    artisanat = models.ForeignKey(
        Artisanat, on_delete=models.CASCADE, related_name='responsable', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.nom_produit_artisanal}) - {self.artisanat.responsable_artisanat.email}'


class Panier(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name='panier')
    produits = models.ManyToManyField(ProduitArtisanal, through='ItemPanier')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Panier de {self.client.username}"


class ItemPanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(ProduitArtisanal, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def sous_total(self):
        return self.produit.prix_artisanat * self.quantite

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom_artisanat} dans le panier de {self.panier.client.username}"


class Commande(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='commandes')
    panier = models.OneToOneField(
        Panier, on_delete=models.CASCADE, null=True, blank=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('Livré', 'Livré'),
        ('Annulé', 'Annulé')
    ], default='En attente')

    def save(self, *args, **kwargs):
        if not self.panier:
            raise ValueError("Un panier est requis pour passer une commande.")
        self.prix_total = self.panier.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.client.email} - {self.date_commande}"
