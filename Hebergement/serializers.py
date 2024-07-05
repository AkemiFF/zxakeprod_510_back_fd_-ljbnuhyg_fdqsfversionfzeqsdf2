# Hebergement/serializers.py
from rest_framework import serializers
from Hebergement.models import *


class ImageChambreSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageChambre
        fields = ('id', 'images', 'couverture', 'legende_chambre', 'image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.images.url)
    
class HebergementSerializer(serializers.ModelSerializer):
    class Meta:
        models = Hebergement
        
        fields = '__all__'