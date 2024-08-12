from rest_framework import serializers
from .models import (
    LocalisationArtisanat,
    ResponsableEtablissement,
    Panier,
    ItemPanier,
    Artisanat,
    ProduitArtisanal,
    Commande,
    Client,
    Specification,
    AvisClientProduitArtisanal,
    ImageProduitArtisanal,
)
from Accounts.models import Client as AccountClient
from Hebergement.models import Localisation
from django.contrib.auth import get_user_model

User = get_user_model()


class LocalisationArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalisationArtisanat
        fields = [
            "adresse",
            "ville",
            "latitude",
            "longitude",
        ]


class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = "__all__"


class ItemPanierSerializer(serializers.ModelSerializer):
    produit = serializers.SerializerMethodField()

    class Meta:
        model = ItemPanier
        fields = ["produit", "quantite"]

    def get_produit(self, obj):
        return ProduitArtisanalSerializer(obj.produit).data


class PanierSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    produits = ItemPanierSerializer(source="itempanier_set", many=True)

    class Meta:
        model = Panier
        fields = ["client", "produits", "total"]


class ArtisanatDetailSerializer(serializers.ModelSerializer):
    localisation_artisanat = LocalisationArtisanatSerializer(read_only=True)

    class Meta:
        model = Artisanat
        fields = [
            "nom",
            "responsable",
            "localisation_artisanat",
        ]


class ShortImageProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduitArtisanal
        fields = ["image", "couverture"]


class ProduitArtisanalSerializer(serializers.ModelSerializer):
    artisanat = ArtisanatDetailSerializer()
    images = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = ProduitArtisanal
        fields = [
            "id",
            "artisanat",
            "images",
            "total_likes",
            "nom_produit_artisanal",
            "description_artisanat",
            "prix_artisanat",
            "disponible_artisanat",
            "nb_produit_dispo",
            "created_at",
            "updated_at",
            "specifications",
            "likes",
        ]

    def get_images(self, obj):
        images = obj.images.all()
        sorted_images = sorted(images, key=lambda x: (not x.couverture, x.id))
        return ShortImageProduitArtisanalSerializer(sorted_images, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["total_likes"] = instance.total_likes()
        return representation


class CommandeSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    panier = PanierSerializer()

    class Meta:
        model = Commande
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    total_commandes = serializers.SerializerMethodField()
    produits_commandes = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "username",
            "email",
            "numero_client",
            "total_commandes",
            "produits_commandes",
        ]

    def get_total_commandes(self, obj):
        return obj.commandes.count()

    def get_produits_commandes(self, obj):
        # Obtenir les paniers associés aux commandes du client
        paniers = Panier.objects.filter(client=obj)

        # Obtenir les produits associés à ces paniers via ItemPanier
        produits = ProduitArtisanal.objects.filter(
            itempanier__panier__in=paniers
        ).distinct()

        return ProduitArtisanalSerializer(produits, many=True).data


class CommandeProduitSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    panier = PanierSerializer(read_only=True)

    class Meta:
        model = Commande
        fields = ["id", "client", "prix_total", "date_commande", "status", "panier"]


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = "__all__"


class ArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisanat
        fields = "__all__"


class AvisClientProduitArtisanalSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()

    class Meta:
        model = AvisClientProduitArtisanal
        fields = ["utilisateur", "note", "commentaire", "created_at"]


class ImageProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduitArtisanal
        fields = ["image"]


class ProduitArtisanalDetailSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True, read_only=True)
    avis_clients = AvisClientProduitArtisanalSerializer(many=True, read_only=True)
    images = ImageProduitArtisanalSerializer(many=True, read_only=True)
    artisanat = ArtisanatDetailSerializer(read_only=True)
    commandes = serializers.SerializerMethodField()

    class Meta:
        model = ProduitArtisanal
        fields = [
            "id",
            "nom_produit_artisanal",
            "description_artisanat",
            "prix_artisanat",
            "disponible_artisanat",
            "specifications",
            "artisanat",
            "nb_produit_dispo",
            "created_at",
            "updated_at",
            "avis_clients",
            "images",
            "commandes",
        ]

    def get_commandes(self, obj):
        commandes = Commande.objects.filter(panier__itempanier__produit=obj)
        return CommandeSerializer(commandes, many=True).data
