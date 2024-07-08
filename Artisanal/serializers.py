from rest_framework import serializers
from Artisanal.models import Artisanat,ProduitArtisanal,Panier,ItemPanier,Commande  # Assurez-vous d'importer Commande depuis Artisanal.models

class ArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisanat
        fields = (
            'responsable_artisanat', 'localisation'
        )

class ProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitArtisanal
        fields = (
            'description_artisanat', 'prix_artisanat', 'disponible_artisanat', 'image_artisanat', 'responsable', 'created_at', 'updated_at'
        )

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = (
            'client', 'produits', 'total'
        )

class ItemPanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPanier
        fields = (
            'panier', 'produit', 'quantite'
        )

class CommandeSerializer(serializers.ModelSerializer):  # Utilisez serializers.ModelSerializer ici
    class Meta:
        model = Commande
        fields = (
            'client', 'panier', 'prix_total', 'date_commande', 'status'
        )
