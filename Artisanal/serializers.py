from rest_framework import serializers
from .models import *
from Accounts.models import *
from Hebergement.models import Localisation
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class ProduitCommandeSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    statut_commande = serializers.SerializerMethodField()
    date_commande = serializers.SerializerMethodField()
    id_commande = serializers.SerializerMethodField()

    class Meta:
        model = ItemPanier
        fields = [
            "id_commande",
            "produit",
            "quantite",
            "client",
            "statut_commande",
            "date_commande",
            "id_commande",
        ]

    def get_client(self, obj):
        return {
            "nom": obj.panier.client.username,
            "email": obj.panier.client.email,
            "telephone": obj.panier.client.numero_client,
        }

    def get_statut_commande(self, obj):
        return obj.panier.commande.status

    def get_date_commande(self, obj):
        date_commande = obj.panier.commande.date_commande
        if isinstance(date_commande, datetime):
            return date_commande.strftime("%d-%m-%Y")  # Format jour-mois-année
        return None

    def get_id_commande(self, obj):
        id_commande = obj.panier.commande.id
        if id_commande:
            return id_commande  # Format jour-mois-année


class ArtisanatCommandeSerializer(serializers.ModelSerializer):
    commandes = serializers.SerializerMethodField()

    class Meta:
        model = ProduitArtisanal
        fields = [
            "nom_produit_artisanal",
            "commandes",
            "prix_artisanat",
        ]

    def get_commandes(self, obj):
        items = ItemPanier.objects.filter(produit=obj, panier__commande__status=False)
        return ProduitCommandeSerializer(items, many=True).data


class ShortCommandeSerializer(serializers.ModelSerializer):
    panier = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Commande
        fields = ["client", "panier", "total"]

    def get_panier(self, obj):
        items = ItemPanier.objects.filter(panier=obj.panier)
        return ShortItemPanierSerializer(items, many=True).data

    def get_total(self, obj):
        return obj.panier.total


class ClientSerializer(serializers.ModelSerializer):
    commandes = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "username", "email", "numero_client", "commandes"]

    def get_commandes(self, obj):
        commandes = Commande.objects.filter(client=obj)
        return ShortCommandeSerializer(commandes, many=True).data


class NewClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "email", "numero_client"]


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


class FieldsProduitArtisanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitArtisanal
        fields = "__all__"


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
    client = NewClientSerializer()
    panier = PanierSerializer()

    class Meta:
        model = Commande
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = "__all__"


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = ["id", "username", "email", "ban"]


class ArtisanatSerializer(serializers.ModelSerializer):
    responsable = ResponsableSerializer()
    total_produits = serializers.SerializerMethodField()

    class Meta:
        model = Artisanat
        fields = "__all__"

    def get_total_produits(self, obj):
        return ProduitArtisanal.objects.filter(artisanat=obj).count()


class TransactionArtisanatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionArtisanat
        fields = "__all__"


class CommandeProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeProduit
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


class ImageProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduitArtisanal
        fields = "__all__"


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


class NProduitArtisanalSerializer(serializers.ModelSerializer):
    images = ImageProduitArtisanalSerializer(many=True, read_only=True)

    class Meta:
        model = ProduitArtisanal
        fields = "__all__"


class eeeItemPanierSerializer(serializers.ModelSerializer):
    produit = NProduitArtisanalSerializer()

    class Meta:
        model = ItemPanier
        fields = ["produit", "quantite"]


class DetailCommandeSerializer(serializers.ModelSerializer):
    client = NewClientSerializer()
    items = eeeItemPanierSerializer(source="panier.itempanier_set", many=True)
    date_commande = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = Commande
        fields = ["id", "client", "items", "prix_total", "date_commande", "status"]
