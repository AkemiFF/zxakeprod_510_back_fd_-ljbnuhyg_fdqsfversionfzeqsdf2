from rest_framework import serializers
# Assurez-vous d'importer Commande depuis Artisanal.models
from Artisanal.models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande


class ArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisanat
        fields = (
            'id', 'responsable_artisanat', 'localisation'
        )


class ProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitArtisanal
        fields = '__all__'


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


# Utilisez serializers.ModelSerializer ici
class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = (
            'client', 'panier', 'prix_total', 'date_commande', 'status'
        )
