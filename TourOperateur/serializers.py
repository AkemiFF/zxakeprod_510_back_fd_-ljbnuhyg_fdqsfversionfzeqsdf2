from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "numero_client", "adresse"]


class TypeTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransport
        fields = "__all__"


class TypeInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInclusion
        fields = "__all__"


class DetailClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "adresse",
            "profilPic",
            "username",
            "email",
            "numero_client",
            "adresse",
        ]


class AvisTourOperateurSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = AvisTourOperateur
        fields = ["id", "client", "note", "commentaire", "date_avis"]


class ImageTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTour
        fields = ["id", "image", "couverture"]


class ImageVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageVoyage
        fields = ["image", "couverture"]


class NewReservationVoyageSerializer(serializers.ModelSerializer):
    client = DetailClientSerializer()

    class Meta:
        model = ReservationVoyage
        fields = ["client", "nombre_voyageurs"]


class VoyageSerializer(serializers.ModelSerializer):
    images_voyage = ImageVoyageSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    inclusions = TypeInclusionSerializer(many=True, read_only=True)
    trajets = serializers.SerializerMethodField()
    all_inclusions = serializers.SerializerMethodField()
    tour_operateur = serializers.SerializerMethodField()
    clients = serializers.SerializerMethodField()

    class Meta:
        model = Voyage
        fields = [
            "id",
            "nom_voyage",
            "ville_depart",
            "description_voyage",
            "destination_voyage",
            "date_debut",
            "date_fin",
            "prix_voyage",
            "places_disponibles",
            "created_at",
            "updated_at",
            "type_transport",
            "images_voyage",
            "likes",
            "inclusions",
            "trajets",
            "nb_like",
            "all_inclusions",
            "tour_operateur",
            "clients",
        ]

    def get_likes(self, obj):
        return VoyageLikeSerializer(obj.likes.all(), many=True).data

    def get_trajets(self, obj):
        return TrajetVoyageSerializer(obj.voyage_trajet.all(), many=True).data

    def get_all_inclusions(self, obj):
        all_inclusions = TypeInclusion.objects.all()
        return TypeInclusionSerializer(all_inclusions, many=True).data

    def get_tour_operateur(self, obj):
        return MiniTourOperateurSerializer(obj.tour_operateur).data

    def get_clients(self, obj):
        reservations = ReservationVoyage.objects.filter(voyage=obj)
        return ReservationVoyageSerializer(reservations, many=True).data


class AllVoyageSerializer(serializers.ModelSerializer):
    nom_tour_operateur = serializers.CharField(
        source="tour_operateur.nom_operateur", read_only=True
    )
    nom_type_transport = serializers.CharField(
        source="type_transport.nom_type", read_only=True
    )
    couverture_images = ImageVoyageSerializer(
        source="get_couverture_images", many=True, read_only=True
    )

    class Meta:
        model = Voyage
        fields = [
            "id",
            "nom_voyage",
            "ville_depart",
            "destination_voyage",
            "description_voyage",
            "date_debut",
            "date_fin",
            "prix_voyage",
            "places_disponibles",
            "created_at",
            "updated_at",
            "tour_operateur",
            "type_transport",
            "nom_tour_operateur",
            "nom_type_transport",
            "distance",
            "couverture_images",
        ]


class PopularVoyageSerializer(serializers.ModelSerializer):
    nom_tour_operateur = serializers.CharField(
        source="tour_operateur.nom_operateur", read_only=True
    )
    nom_type_transport = serializers.CharField(
        source="type_transport.nom_type", read_only=True
    )
    couverture_images = ImageVoyageSerializer(
        source="get_couverture_images", many=True, read_only=True
    )
    like_count = serializers.IntegerField(source="nb_like", read_only=True)

    class Meta:
        model = Voyage
        fields = [
            "id",
            "nom_voyage",
            "ville_depart",
            "destination_voyage",
            "description_voyage",
            "date_debut",
            "date_fin",
            "prix_voyage",
            "places_disponibles",
            "created_at",
            "updated_at",
            "tour_operateur",
            "type_transport",
            "nom_tour_operateur",
            "nom_type_transport",
            "couverture_images",
            "like_count",
        ]


class SatisfactionClientSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = SatisfactionClient
        fields = ["client", "est_satisfait"]


class TourOperateurSerializer(serializers.ModelSerializer):
    avis_tour_operateur = AvisTourOperateurSerializer(many=True, read_only=True)
    images_tour = serializers.SerializerMethodField()
    voyages = VoyageSerializer(many=True, read_only=True)
    nombre_voyages = serializers.SerializerMethodField()
    nombre_satisfactions = serializers.SerializerMethodField()
    nombre_avis = serializers.SerializerMethodField()

    class Meta:
        model = TourOperateur
        fields = [
            "id",
            "nom_operateur",
            "responsable_TourOperateur",
            "adresse_operateur",
            "email_operateur",
            "telephone_operateur",
            "description_operateur",
            "created_at",
            "updated_at",
            "avis_tour_operateur",
            "images_tour",
            "voyages",
            "nombre_voyages",
            "nombre_satisfactions",
            "nombre_avis",
        ]

    def get_nombre_voyages(self, obj):
        return obj.voyages.count()

    def get_nombre_avis(self, obj):
        return obj.avis_tour_operateur.count()

    def get_nombre_satisfactions(self, obj):
        return obj.tour_satisfaction.filter(est_satisfait=True).count()

    def get_images_tour(self, obj):
        images = obj.images_tour.all()
        sorted_images = sorted(images, key=lambda img: not img.couverture)
        return ImageTourSerializer(sorted_images, many=True).data


class VoyageLikeSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = VoyageLike
        fields = ["client"]


class InclusionVoyageSerializer(serializers.ModelSerializer):
    nom_type_inclusion = serializers.SerializerMethodField()

    class Meta:
        model = InclusionVoyage
        fields = ["id", "voyage", "type_inclusion", "nom_type_inclusion"]

    def get_nom_type_inclusion(self, obj):
        return obj.type_inclusion.nom_inclusion


class TrajetVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrajetVoyage
        fields = ["numero_trajet", "nom_ville", "date_trajet", "description_trajet"]


class LocalisationTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalisationTour
        fields = "__all__"


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "numero_client", "adresse"]


class MiniTourOperateurSerializer(serializers.ModelSerializer):
    images_tour = serializers.SerializerMethodField()
    localisation = LocalisationTourSerializer(
        read_only=True, source="localisation_tour"
    )

    class Meta:
        model = TourOperateur
        fields = [
            "id",
            "nom_operateur",
            "adresse_operateur",
            "localisation",
            "email_operateur",
            "description_operateur",
            "images_tour",
        ]

    def get_images_tour(self, obj):
        images = obj.images_tour.all()
        sorted_images = sorted(images, key=lambda img: not img.couverture)
        return ImageTourSerializer(sorted_images, many=True).data


class VoyageListSerializer(serializers.ModelSerializer):
    images_voyage = ImageVoyageSerializer(many=True, read_only=True)
    list_travelers = serializers.SerializerMethodField()

    class Meta:
        model = Voyage
        fields = "__all__"

    def get_list_travelers(self, obj):
        reservations = ReservationVoyage.objects.filter(voyage=obj)
        return ReservationVoyageSerializer(reservations, many=True).data


class ReservationVoyageSerializer(serializers.ModelSerializer):
    client = ClientListSerializer(read_only=True)

    class Meta:
        model = ReservationVoyage
        fields = ["voyage", "client", "date_reservation_voyage", "status"]

    def get_clients_list(self, obj):
        client_list = Client.objects.filter(id=obj)
        return ClientListSerializer(client_list, many=True).data


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "numero_client", "adresse"]

    def get_list_client(self, obj):
        list_client = Client.objects.filter(voyage=obj)
        return ReservationVoyageSerializer(list_client, many=True).data


class ShortVoyageSerializer(serializers.ModelSerializer):
    reservations = NewReservationVoyageSerializer(many=True, read_only=True)

    class Meta:
        model = Voyage
        fields = [
            "id",
            "nom_voyage",
            "ville_depart",
            "destination_voyage",
            "reservations",
        ]


class CreateVoyageSerializer(serializers.ModelSerializer):
    inclusions = serializers.PrimaryKeyRelatedField(
        queryset=InclusionVoyage.objects.all(), many=True, required=False
    )
    images = serializers.PrimaryKeyRelatedField(
        queryset=ImageVoyage.objects.all(), many=True, required=False
    )
    tour_operateur = serializers.PrimaryKeyRelatedField(
        queryset=TourOperateur.objects.all()
    )

    class Meta:
        model = Voyage
        fields = [
            "id",
            "nom_voyage",
            "ville_depart",
            "destination_voyage",
            "description_voyage",
            "date_debut",
            "date_fin",
            "distance",
            "prix_voyage",
            "places_disponibles",
            "type_transport",
            "inclusions",
            "images",
            "tour_operateur",
        ]

    def create(self, validated_data):
        inclusions_ids = validated_data.pop("inclusions", [])
        images_ids = validated_data.pop("images", [])
        print(inclusions_ids)

        voyage = Voyage.objects.create(**validated_data)

        # Associer les inclusions
        if inclusions_ids:
            for inclusion_id in inclusions_ids:
                inclusion = TypeInclusion.objects.get(nom_inclusion=inclusion_id)
                voyage.inclusions.add(inclusion)

        # Associer les images
        if images_ids:
            for image_id in images_ids:
                image = ImageVoyage.objects.get(id=image_id)
                voyage.images_voyage.add(image)
        return voyage


class ListVoyageSerializer(serializers.ModelSerializer):
    type_transport_info = serializers.SerializerMethodField()
    confirmed_booking = serializers.SerializerMethodField()
    pending_booking = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Voyage
        fields = [
            "id",
            "confirmed_booking",
            "pending_booking",
            "images",
            "nom_voyage",
            "ville_depart",
            "destination_voyage",
            "description_voyage",
            "date_debut",
            "date_fin",
            "distance",
            "prix_voyage",
            "places_disponibles",
            "created_at",
            "updated_at",
            "tour_operateur",
            "type_transport",
            "inclusions",
            "type_transport_info",
        ]

    def get_confirmed_booking(self, obj):
        reservations = ReservationVoyage.objects.filter(voyage=obj)

        confirmed_bookings = reservations.filter(status="confirmed")

        return confirmed_bookings.count()

    def get_pending_booking(self, obj):
        reservations = ReservationVoyage.objects.filter(voyage=obj)

        pending_booking = reservations.filter(status="pending")

        return pending_booking.count()

    def get_images(self, obj):

        images = ImageVoyage.objects.filter(image_voyage=obj)
        return ImageVoyageSerializer(images, many=True).data

    def get_type_transport_info(self, obj):
        if obj.type_transport:
            serializer = TypeTransportSerializer(obj.type_transport)
            return serializer.data
        return None
