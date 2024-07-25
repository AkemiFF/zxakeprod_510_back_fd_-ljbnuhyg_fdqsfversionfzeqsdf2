from rest_framework import serializers
from .models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande
from Accounts.models import *
from Hebergement.models import Localisation
from django.contrib.auth import get_user_model

User = get_user_model()

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['id', 'adresse']  # Adjust fields as needed

class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = ['id', 'email']  # Adjust fields as needed

class ArtisanatSerializer(serializers.ModelSerializer):
    responsable_artisanat = ResponsableEtablissementSerializer()
    localisation = LocalisationSerializer()

    class Meta:
        model = Artisanat
        fields = ['id', 'responsable_artisanat', 'localisation']

class ProduitArtisanalSerializer(serializers.ModelSerializer):
    artisanat = ArtisanatSerializer()

    class Meta:
        model = ProduitArtisanal
        fields = ['id', 'nom_produit_artisanal', 'description_artisanat', 'prix_artisanat', 'disponible_artisanat', 'image_artisanat', 'artisanat', 'created_at', 'updated_at']

class PanierSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()  # or use ClientSerializer if you need detailed info
    produits = serializers.StringRelatedField(many=True)  # or use ProduitArtisanalSerializer if detailed info is needed

    class Meta:
        model = Panier
        fields = ['id', 'client', 'produits', 'total']

class ItemPanierSerializer(serializers.ModelSerializer):
    panier = PanierSerializer()
    produit = ProduitArtisanalSerializer()

    class Meta:
        model = ItemPanier
        fields = ['id', 'panier', 'produit', 'quantite']

class CommandeSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()  # or use ClientSerializer if you need detailed info
    panier = PanierSerializer()

    class Meta:
        model = Commande
        fields = ['id', 'client', 'panier', 'prix_total', 'date_commande', 'status']
