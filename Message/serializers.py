# serializers.py

from rest_framework import serializers
from .models import HebergementMessage, ArtisanatMessage, TourOperateurMessage

class HebergementMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementMessage
        fields = '__all__'

class ArtisanatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanatMessage
        fields = '__all__'

class TourOperateurMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperateurMessage
        fields = '__all__'
