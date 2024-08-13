from Accounts.models import Client
from django.conf import settings
from django.db import models
from Accounts.models import *
from django.core.exceptions import ValidationError

from Hebergement.models import Localisation


class Specification(models.Model):
    type_specification = models.CharField(max_length=300, null=True, unique=True)

    def __str__(self) -> str:
        return self.type_specification


class Artisanat(models.Model):
    nom = models.CharField(max_length=200, null=True, blank=True)

    responsable = models.ForeignKey(
        ResponsableEtablissement,
        on_delete=models.CASCADE,
        related_name="artisanat_responsable",
    )
    telephone = models.CharField(max_length=15, null=True, blank=True)

    stat = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    email = models.EmailField(max_length=400, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.responsable} ({self.nom})"


class LocalisationArtisanat(models.Model):
    adresse = models.CharField(max_length=200, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    artisanat = models.OneToOneField(
        Artisanat,
        on_delete=models.CASCADE,
        related_name="localisation_artisanat",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.adresse


class ProduitArtisanal(models.Model):
    nom_produit_artisanal = models.CharField(max_length=100, default="")
    description_artisanat = models.TextField()
    prix_artisanat = models.DecimalField(max_digits=8, decimal_places=2)
    disponible_artisanat = models.BooleanField(default=True)
    specifications = models.ManyToManyField(
        "Specification", related_name="produits_artisanaux"
    )

    artisanat = models.ForeignKey(
        Artisanat,
        on_delete=models.CASCADE,
        related_name="responsable_produit",
        null=True,
        blank=True,
    )
    nb_produit_dispo = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(Client, related_name="liked_produits", blank=True)

    def __str__(self):
        return f"({self.nom_produit_artisanal}) - {self.artisanat.responsable.email}"

    def total_likes(self):
        return self.likes.count()


class AvisClientProduitArtisanal(models.Model):
    produit = models.ForeignKey(
        ProduitArtisanal, on_delete=models.CASCADE, related_name="avis_clients"
    )
    utilisateur = models.ForeignKey(Client, on_delete=models.CASCADE)
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avis de {self.utilisateur.username} pour {self.produit.nom_produit_artisanal}"


class ImageProduitArtisanal(models.Model):
    produit = models.ForeignKey(
        ProduitArtisanal,
        on_delete=models.CASCADE,
        related_name="images",
    )
    couverture = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/artisanat_images", blank=True)

    def __str__(self):
        return f"Image for {self.produit.nom_produit_artisanal}"


class Panier(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name="panier"
    )
    produits = models.ManyToManyField(ProduitArtisanal, through="ItemPanier")
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
        return f"{self.quantite} x {self.produit.nom_produit_artisanal} dans le panier de {self.panier.client.username}"


class Commande(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="commandes"
    )
    panier = models.OneToOneField(
        Panier, on_delete=models.CASCADE, null=True, blank=True
    )
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("En attente", "En attente"),
            ("En cours", "En cours"),
            ("Livré", "Livré"),
            ("Annulé", "Annulé"),
        ],
        default="En attente",
    )

    def save(self, *args, **kwargs):
        if not self.panier:
            raise ValueError("Un panier est requis pour passer une commande.")
        self.prix_total = self.panier.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.client.email} - {self.date_commande}"
