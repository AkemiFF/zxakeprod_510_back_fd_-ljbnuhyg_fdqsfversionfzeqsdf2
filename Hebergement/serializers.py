from rest_framework import serializers
from Hebergement.models import Hebergement, HebergementImage

class HebergementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementImage
        fields = ['id', 'hebergement', 'couverture', 'legende_hebergement', 'created_at', 'updated_at']

class HebergementSerializer(serializers.ModelSerializer):
    images = HebergementImageSerializer(many=True, read_only=True)
    image_files = serializers.ListField(
        child=serializers.ImageField(write_only=True), write_only=True, required=False
    )

    class Meta:
        model = Hebergement
        fields = ['id', 'nom_hebergement', 'description_hebergement', 'nombre_etoile_hebergement', 'responsable_hebergement', 'type_hebergement', 'created_at', 'updated_at', 'images', 'image_files']

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        hebergement = Hebergement.objects.create(**validated_data)
        for image_file in image_files:
            HebergementImage.objects.create(hebergement=hebergement, images=image_file)
        return hebergement
