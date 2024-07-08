from rest_framework import serializers
from .models import TourOperateur, Voyage, ImageVoyage, Reservation_voyage
from Accounts.serializers import ResponsableEtablissementSerializer, ClientSerializer


class TourOperateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperateur
        fields = (
            'id', 'nom_operateur', 'responsable_TourOperateur', 'adresse_operateur', 'email_operateur', 'telephone_operateur',
            'description_operateur', 'image_tour', 'created_at', 'updated_at'
        )

class VoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voyage
        fields = (
            'id', 'tour_operateur', 'nom_voyage', 'description_voyage', 'destination_voyage', 'date_debut', 'date_fin',
            'prix_voyage', 'places_disponibles', 'created_at', 'updated_at'
        )

class ImageVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageVoyage
        fields = (
            'id', 'voyage', 'image', 'description'
        )

class ReservationVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_voyage
        fields = (
            'id', 'voyage', 'client', 'date_reservation_voyage', 'status'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation

    def create(self, validated_data):
        return Reservation_voyage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.voyage = validated_data.get('voyage', instance.voyage)
        instance.client = validated_data.get('client', instance.client)
        instance.date_reservation_voyage = validated_data.get('date_reservation_voyage', instance.date_reservation_voyage)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
