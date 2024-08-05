from rest_framework import serializers
from Hebergement.models import *
from django.db.models import Min
from Accounts.serializers import ClientSerializer
from django.db.models import Avg


class SuggestionHebergementSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    note_moyenne = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Hebergement
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        couverture_image = obj.images.filter(couverture=True).first()
        if couverture_image:    
            absolute_url = request.build_absolute_uri(couverture_image.image.url)
            return absolute_url

        return None

    def get_ville(self, obj):
        try:
            localisation = obj.localisation
            ville = f"{localisation.ville} , {localisation.adresse}"
            return ville
        except Localisation.DoesNotExist:
            return None

    def get_note_moyenne(self, obj):
        avis = obj.avis_hotel.all()
        if avis.exists():
            moyenne = avis.aggregate(average_note=Avg("note"))["average_note"]
            return moyenne if moyenne is not None else 0
        return 0


class HebergementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementImage
        fields = "__all__"


class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = "__all__"


class HebergementSerializer(serializers.ModelSerializer):
    min_prix_nuit_chambre = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    localisation = LocalisationSerializer()
    image_files = serializers.ListField(
        child=serializers.ImageField(write_only=True), write_only=True, required=False
    )
    nombre_avis = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()

    def get_min_prix_nuit_chambre(self, instance):
        min_price = HebergementChambre.objects.filter(hebergement=instance).aggregate(
            Min("prix_nuit_chambre")
        )["prix_nuit_chambre__min"]
        return min_price

    def get_accessoires(self, instance):
        accessoires = HebergementAccessoire.objects.filter(hebergement=instance)
        return accessoires

    def get_images(self, obj):
        images = obj.images.all().order_by("-couverture", "id")
        return HebergementImageSerializer(images, many=True).data

    def get_localisation(self, instance):
        localisation = instance.localisation
        if localisation:
            return {
                "adresse": localisation.adresse,
                "ville": localisation.ville,
                "latitude": localisation.latitude,
                "longitude": localisation.longitude,
            }
        return None

    def get_nombre_avis(self, instance):
        return instance.avis_hotel.count()

    class Meta:
        model = Hebergement
        fields = [
            "id",
            "total_likes",
            "nom_hebergement",
            "nombre_avis",
            "localisation",
            "description_hebergement",
            "min_prix_nuit_chambre",
            "nombre_etoile_hebergement",
            "responsable_hebergement",
            "type_hebergement",
            "created_at",
            "updated_at",
            "images",
            "image_files",
            "accessoires",
        ]

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", [])
        hebergement = Hebergement.objects.create(**validated_data)

        for image_file in image_files:
            HebergementImage.objects.create(hebergement=hebergement, image=image_file)

        return hebergement


class TypeHebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeHebergement
        fields = "__all__"


class AccessoireHebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoireHebergement
        fields = "__all__"


class ImageChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageChambre
        fields = "__all__"


class ChambreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chambre
        fields = "__all__"


class ChambrePersonaliserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChambrePersonaliser
        fields = "__all__"


class AccessoireChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoireChambre
        fields = "__all__"


class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = "__all__"


class HebergementAccessoireSerializer(serializers.ModelSerializer):
    accessoire = AccessoireHebergementSerializer()

    class Meta:
        model = HebergementAccessoire
        fields = "__all__"


class HebergementAccessoireSerializerID(serializers.ModelSerializer):
    class Meta:
        model = HebergementAccessoire
        fields = ["hebergement", "accessoire"]


class HebergementChambreAccessoireSerializer(serializers.ModelSerializer):
    accessoire_chambre = AccessoireChambreSerializer()

    class Meta:
        model = HebergementChambreAccessoire
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class AvisClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvisClients
        fields = "__all__"


class HebergementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementImage
        fields = "__all__"


# class TypeAccessoireSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TypeAccessoire
#         fields = ["nom_type"]

from rest_framework import serializers
from .models import HebergementChambre, Reservation
from .serializers import (
    ChambreSerializer,
    ChambrePersonaliserSerializer,
    AccessoireChambreSerializer,
    ImageChambreSerializer,
    ReservationSerializer,
)


class HebergementChambreSerializer(serializers.ModelSerializer):
    chambre = ChambreSerializer()
    chambre_personaliser = ChambrePersonaliserSerializer()
    accessoires = AccessoireChambreSerializer(many=True)
    images_chambre = ImageChambreSerializer(many=True, read_only=True)
    reservation = serializers.SerializerMethodField()

    class Meta:
        model = HebergementChambre
        fields = "__all__"

    def get_reservation(self, obj):
        # Assurez-vous que 'chambre_reserve' est la bonne relation dans le modèle Reservation
        reservation = Reservation.objects.filter(chambre_reserve=obj)
        serializer = ReservationSerializer(reservation, many=True)
        return serializer.data


class TypeAccessoireSerializer(serializers.ModelSerializer):
    accessoires = serializers.SerializerMethodField()

    class Meta:
        model = TypeAccessoire
        fields = ["nom_type", "accessoires"]

    def get_accessoires(self, obj):
        accessoires = AccessoireHebergement.objects.filter(type_accessoire=obj)
        return AccessoireHebergementSerializer(accessoires, many=True).data


class AccessoireSerializer(serializers.ModelSerializer):
    type_accessoire_nom = serializers.SerializerMethodField()

    class Meta:
        model = AccessoireHebergement
        fields = "__all__"
        extra_kwargs = {
            "type_accessoire": {"write_only": True},
        }

    def get_type_accessoire_nom(self, obj):
        if obj.type_accessoire:
            return obj.type_accessoire.nom_type
        return None


class TypeAccessoireSerializer(serializers.ModelSerializer):
    accessoires = serializers.SerializerMethodField()

    class Meta:
        model = TypeAccessoire
        fields = ["nom_type", "accessoires"]

    def get_accessoires(self, obj):
        accessoires = AccessoireHebergement.objects.filter(type_accessoire=obj)
        return AccessoireHebergementSerializer(accessoires, many=True).data


class TypeAccessoireSerializer2(serializers.ModelSerializer):
    accessoires = serializers.SerializerMethodField()

    class Meta:
        model = TypeAccessoire
        fields = "__all__"

    def get_accessoires(self, obj):
        hebergement_id = self.context.get("hebergement_id")

        if hebergement_id:
            hebergement_accessoires = HebergementAccessoire.objects.filter(
                hebergement_id=hebergement_id
            )
            accessoires = AccessoireHebergement.objects.filter(
                hebergementaccessoire__in=hebergement_accessoires
            )

        return AccessoireSerializer(accessoires, many=True).data


class OwnAccessoireHebergementSerializer(serializers.ModelSerializer):
    type_accessoire_nom = serializers.SerializerMethodField()

    class Meta:
        model = AccessoireHebergement
        fields = "__all__"
        # Ajoutez 'type_accessoire_nom' si vous souhaitez qu'il apparaisse
        extra_kwargs = {
            "type_accessoire": {
                "write_only": True
            },  # Masquer le champ `type_accessoire` si nécessaire
        }

    def get_type_accessoire_nom(self, obj):
        if obj.type_accessoire:
            return obj.type_accessoire.nom_type
        return None


class HebergementSerializerAll(serializers.ModelSerializer):

    type_hebergement = TypeHebergementSerializer()
    images = serializers.SerializerMethodField()
    chambres = HebergementChambreSerializer(many=True, source="hebergementchambre_set")
    localisation = LocalisationSerializer()
    accessoires_haves = serializers.SerializerMethodField()
    accessoires = serializers.SerializerMethodField()
    avis_hotel = AvisClientsSerializer(many=True)

    def get_min_prix_nuit_chambre(self, instance):
        min_price = HebergementChambre.objects.filter(hebergement=instance).aggregate(
            Min("prix_nuit_chambre")
        )["prix_nuit_chambre__min"]
        return min_price

    def get_images(self, obj):
        images = obj.images.all().order_by("-couverture", "id")
        return HebergementImageSerializer(images, many=True).data

    def get_accessoires(self, obj):
        type_accessoires = TypeAccessoire.objects.all()
        serializer = TypeAccessoireSerializer(type_accessoires, many=True)
        data = {}
        for item in serializer.data:
            type_nom = item["nom_type"]
            accessoires = [acc for acc in item["accessoires"]]
            data[type_nom] = accessoires
        return data

    def get_accessoires_haves(self, obj):
        hebergement_accessoires = HebergementAccessoire.objects.filter(
            hebergement=obj.id
        )
        accessoires = AccessoireHebergement.objects.filter(
            hebergementaccessoire__in=hebergement_accessoires
        )

        serializer = OwnAccessoireHebergementSerializer(
            accessoires, many=True, context={"hebergement_id": obj.id}
        )

        return serializer.data

    class Meta:
        model = Hebergement
        fields = "__all__"


from rest_framework import serializers
from .models import AvisClients, Client, Localisation


class SecondLocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ["adresse", "ville"]


class HebergementWithLocalisationSerializer(serializers.ModelSerializer):
    localisation = SecondLocalisationSerializer()  # Utiliser le related_name

    class Meta:
        model = Hebergement
        fields = ["nom_hebergement", "localisation"]


class AllAvisClientsSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    hebergement = HebergementWithLocalisationSerializer()

    class Meta:
        model = AvisClients
        fields = [
            "id",
            "client",
            "commentaire",
            "note",
            "created_at",
            "updated_at",
            "hebergement",
        ]


class GetChambreSerializer(serializers.ModelSerializer):
    images_chambre = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )
    accessoires = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    images = ImageChambreSerializer(many=True, read_only=True)
    accessoires_list = HebergementChambreAccessoireSerializer(
        many=True, read_only=True, source="hebergementchambreaccessoire_set"
    )

    class Meta:
        model = HebergementChambre
        fields = "__all__"


class EditChambreSerializer(serializers.ModelSerializer):
    images_chambre = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )
    accessoires = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    images = ImageChambreSerializer(many=True, read_only=True)
    accessoires_list = HebergementChambreAccessoireSerializer(
        many=True, read_only=True, source="hebergementchambreaccessoire_set"
    )

    class Meta:
        model = HebergementChambre
        fields = "__all__"

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images_chambre", [])
        accessoires_data = validated_data.pop("accessoires", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if images_data:
            instance.images.all().delete()  # Delete existing images if new ones are provided
            for image_data in images_data:
                ImageChambre.objects.create(
                    hebergement_chambre=instance, images=image_data
                )

        if accessoires_data:
            instance.hebergementchambreaccessoire_set.all().delete()  # Delete existing accessories if new ones are provided
            for i in accessoires_data:
                try:
                    accessoire = AccessoireChambre.objects.get(id=i)
                    HebergementChambreAccessoire.objects.create(
                        hebergement_chambre=instance, accessoire_chambre=accessoire
                    )
                except AccessoireChambre.DoesNotExist:
                    raise serializers.ValidationError(
                        f"AccessoireChambre with id {i} does not exist."
                    )

        return instance


class ImageChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageChambre
        fields = ["id", "images"]


class AjoutChambreSerializer(serializers.ModelSerializer):
    images_chambre = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )
    accessoires = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    images = ImageChambreSerializer(many=True, read_only=True)
    accessoires_list = HebergementChambreAccessoireSerializer(
        many=True, read_only=True, source="hebergementchambreaccessoire_set"
    )

    class Meta:
        model = HebergementChambre
        fields = "__all__"

    def create(self, validated_data):
        images_data = validated_data.pop("images_chambre", [])
        accessoires_data = validated_data.pop("accessoires", [])

        hebergement_chambre = HebergementChambre.objects.create(**validated_data)
        for image_data in images_data:
            creation = ImageChambre.objects.create(
                hebergement_chambre=hebergement_chambre, images=image_data
            )

        for i in accessoires_data:
            accessoire = AccessoireChambre.objects.get(id=i)
            HebergementChambreAccessoire.objects.create(
                hebergement_chambre=hebergement_chambre, accessoire_chambre=accessoire
            )

        return hebergement_chambre
