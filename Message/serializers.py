# serializers.py

from rest_framework import serializers

from .models import HebergementMessage, TourOperateurMessage


class HebergementMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementMessage
        fields = '__all__'

class TourOperateurMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperateurMessage
        fields = '__all__'
