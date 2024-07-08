# views.py
# serializers.py

from rest_framework import serializers
from .models import TourOperateur, Voyage, ImageVoyage, Reservation_voyage
from Accounts.serializers import ResponsableEtablissementSerializer, ClientSerializer


class TourOperateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperateur
        fields = '__all__'


class VoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voyage
        fields = '__all__'


class ImageVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageVoyage
        fields = '__all__'


class ReservationVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_voyage
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation


