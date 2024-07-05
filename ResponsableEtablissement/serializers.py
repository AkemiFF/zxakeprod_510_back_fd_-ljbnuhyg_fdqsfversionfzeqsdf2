# yourapp/serializers.py
from rest_framework import serializers
from Accounts.models import ResponsableEtablissement
from django.contrib.auth import authenticate


class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    mdp_responsable = serializers.CharField(write_only=True)

    class Meta:
        model = ResponsableEtablissement
        fields = '__all__'

    def create(self, validated_data):
        responsable = ResponsableEtablissement.objects.create(
            email_responsable=validated_data['email_responsable'],
            nom_responsable=validated_data['nom_responsable'],
            prenom_responsable=validated_data['prenom_responsable'],
            mdp_responsable=validated_data['mdp_responsable'],
            numero_responsable=validated_data['numero_responsable']
        )
        return responsable

# Login


class ResponsableEtablissementLoginSerializer(serializers.Serializer):
    email_responsable = serializers.EmailField()
    mdp_responsable = serializers.CharField()

    def validate(self, data):
        email = data.get('email_responsable')
        password = data.get('mdp_responsable')

        if email and password:
            user = authenticate(email_responsable=email,
                                mdp_responsable=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError(
                    "Email ou mot de passe incorrect.")
        else:
            raise serializers.ValidationError(
                "Email et mot de passe sont requis.")

        return data
