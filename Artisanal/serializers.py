from rest_framework import serializers
from .models import *
from Accounts.models import *
from Hebergement.models import Localisation
from django.contrib.auth import get_user_model

User = get_user_model()


class ShortCommandeSerializer(serializers.ModelSerializer):
    panier = serializers.SerializerMethodField()

    class Meta:
        model = Commande
        fields = ["client", "panier"]

    def get_panier(self, obj):
        items = ItemPanier.objects.filter(panier=obj.panier)
        return ShortItemPanierSerializer(items, many=True).data


class ClientSerializer(serializers.ModelSerializer):
    commandes = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "username", "email", "numero_client", "commandes"]

    def get_commandes(self, obj):
        commandes = Commande.objects.filter(client=obj)
        return ShortCommandeSerializer(commandes, many=True).data


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
        fields = "__all__"  # Adjust fields as needed


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
            # "description_artisanat",
            "responsable",
            "localisation_artisanat",
        ]


class ShortImageProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduitArtisanal
        fields = ["image", "couverture"]


from rest_framework import serializers


class ImageProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduitArtisanal
        fields = ["id", "image", "couverture"]


class ProduitArtisanalSerializer(serializers.ModelSerializer):
    artisanat = ArtisanatDetailSerializer()
    images = ImageProduitArtisanalSerializer(many=True, read_only=True)
    total_likes = serializers.ReadOnlyField()  # Champ readonly pour le nombre de likes

    class Meta:
        model = ProduitArtisanal
        fields = [
            "id",
            "artisanat",
            "images",
            "total_likes",  # Inclure le champ total_likes
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


class ShortProduitArtisanalSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProduitArtisanal
        fields = [
            "id",
            "nom_produit_artisanal",
            "description_artisanat",
            "prix_artisanat",
            "nb_produit_dispo",
        ]

    def get_images(self, obj):
        images = obj.images.all()
        sorted_images = sorted(images, key=lambda x: (not x.couverture, x.id))
        return ShortImageProduitArtisanalSerializer(sorted_images, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ajoute le nombre de likes au dictionnaire de représentation
        representation["total_likes"] = instance.total_likes()
        return representation


"""[
    
 
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
]"""


class ItemPanierSerializer(serializers.ModelSerializer):
    panier = PanierSerializer()
    produit = ProduitArtisanalSerializer()

    class Meta:
        model = ItemPanier
        fields = "__all__"


class ShortItemPanierSerializer(serializers.ModelSerializer):
    produit = ShortProduitArtisanalSerializer()

    class Meta:
        model = ItemPanier
        fields = ["produit", "quantite"]


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
        ]
