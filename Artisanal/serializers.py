from rest_framework import serializers
from .models import *
from Accounts.models import *
from Hebergement.models import Localisation
from django.contrib.auth import get_user_model

User = get_user_model()


class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = "__all__"  # Adjust fields as needed


class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = "__all__"  # Adjust fields as needed


class ArtisanatSerializer(serializers.ModelSerializer):
    responsable_artisanat = ResponsableEtablissementSerializer()
    localisation = LocalisationSerializer()

    class Meta:
        model = Artisanat
        fields = "__all__"


class ProduitArtisanalSerializer(serializers.ModelSerializer):
    artisanat = ArtisanatSerializer()

    class Meta:
        model = ProduitArtisanal
        fields = "__all__"


class PanierSerializer(serializers.ModelSerializer):
    client = (
        serializers.StringRelatedField()
    )  # or use ClientSerializer if you need detailed info
    produits = serializers.StringRelatedField(
        many=True
    )  # or use ProduitArtisanalSerializer if detailed info is needed

    class Meta:
        model = Panier
        fields = "__all__"


class ItemPanierSerializer(serializers.ModelSerializer):
    panier = PanierSerializer()
    produit = ProduitArtisanalSerializer()

    class Meta:
        model = ItemPanier
        fields = "__all__"


class CommandeSerializer(serializers.ModelSerializer):
    client = (
        serializers.StringRelatedField()
    )  # or use ClientSerializer if you need detailed info
    panier = PanierSerializer()

    class Meta:
        model = Commande
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
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


class LocalisationArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalisationArtisanat
        fields = [
            "adresse",
            "ville",
            "latitude",
            "longitude",
        ]


class ArtisanatDetailSerializer(serializers.ModelSerializer):
    localisation_artisanat = LocalisationArtisanatSerializer(read_only=True)

    class Meta:
        model = Artisanat
        fields = [
            "nom_artisanat",
            # "description_artisanat",
            "responsable_artisanat",
            "localisation_artisanat",
        ]


class ProduitArtisanalDetailSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True, read_only=True)
    avis_clients = AvisClientProduitArtisanalSerializer(many=True, read_only=True)
    images = ImageProduitArtisanalSerializer(many=True, read_only=True)
    artisanat = ArtisanatDetailSerializer(read_only=True)

    class Meta:
        model = ProduitArtisanal
        fields = [
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
        ]
