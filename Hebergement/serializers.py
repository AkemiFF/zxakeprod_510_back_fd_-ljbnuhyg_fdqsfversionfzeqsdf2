from rest_framework import serializers
from Hebergement.models import *
from django.db.models import Min

class HebergementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementImage
        fields = '__all__'

class HebergementSerializer(serializers.ModelSerializer):
    min_prix_nuit_chambre = serializers.SerializerMethodField()

    images = serializers.SerializerMethodField()
    image_files = serializers.ListField(
        child=serializers.ImageField(write_only=True), write_only=True, required=False
    )

    def get_min_prix_nuit_chambre(self, instance):
        min_price = HebergementChambre.objects.filter(hebergement=instance).aggregate(Min('prix_nuit_chambre'))['prix_nuit_chambre__min']
        return min_price

    def get_images(self, instance):
        hebergement_images = HebergementImage.objects.filter(hebergement=instance)
        serializer = HebergementImageSerializer(hebergement_images, many=True)
        return serializer.data

    class Meta:
        model = Hebergement
        fields = ['id', 'nom_hebergement', 'description_hebergement', 'min_prix_nuit_chambre', 'nombre_etoile_hebergement', 'responsable_hebergement', 'type_hebergement', 'created_at', 'updated_at', 'images', 'image_files']

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        hebergement = Hebergement.objects.create(**validated_data)

        for image_file in image_files:
            HebergementImage.objects.create(hebergement=hebergement, images=image_file)

        return hebergement





class TypeHebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeHebergement
        fields = '__all__'

class HebergementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementImage
        fields = '__all__'

class AccessoireHebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoireHebergement
        fields = '__all__'

class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambre
        fields = '__all__'

class ChambrePersonaliserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChambrePersonaliser
        fields = '__all__'

class HebergementChambreSerializer(serializers.ModelSerializer):
    chambre = ChambreSerializer()
    chambre_personaliser = ChambrePersonaliserSerializer()
    accessoires = AccessoireHebergementSerializer(many=True)

    class Meta:
        model = HebergementChambre
        fields = '__all__'

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'

class HebergementAccessoireSerializer(serializers.ModelSerializer):
    accessoire = AccessoireHebergementSerializer()

    class Meta:
        model = HebergementAccessoire
        fields = '__all__'

class AccessoireChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoireChambre
        fields = '__all__'

class HebergementChambreAccessoireSerializer(serializers.ModelSerializer):
    accessoire_chambre = AccessoireChambreSerializer()

    class Meta:
        model = HebergementChambreAccessoire
        fields = '__all__'

class ImageChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageChambre
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class AvisClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvisClients
        fields = '__all__'



class HebergementSerializerAll(serializers.ModelSerializer):
    type_hebergement = TypeHebergementSerializer()
    images = HebergementImageSerializer(many=True)
    chambres = HebergementChambreSerializer(many=True, source='hebergementchambre_set')
    localisation = LocalisationSerializer(source='hebergement')    
    accessoires = HebergementAccessoireSerializer(many=True, source='hebergementaccessoire_set')
    reservations = ReservationSerializer(many=True)  # Assurez-vous du nom correct
    avis_hotel = AvisClientsSerializer(many=True)

    class Meta:
        model = Hebergement
        fields = '__all__'
