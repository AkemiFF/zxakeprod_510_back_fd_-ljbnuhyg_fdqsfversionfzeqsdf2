# MyAccount/serialisers.py
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Client
from rest_framework import serializers
from Accounts.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ClientWithEmailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = Client
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializerVerify(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserEmailSerializerVerify(serializers.Serializer):
    email = serializers.EmailField()
    # emailProviderUid = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class InfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "username",
            "email",
            "password",
            "emailProviderId",
            "numero_client",
            "emailProviderUid",
            "emailPhotoUrl",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# Pour le TypeResponsable


class TypeResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeResponsable
        fields = "__all__"


# Pour ResponsableEtablissement


class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "numero_responsable",
            "created_at",
            "updated_at",
            "type_responsable",
        )
        extra_kwargs = {
            "password_responsable": {"write_only": True},
        }


class AddResponsableEtablissementSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    adresse = serializers.CharField(max_length=150, required=False, allow_blank=True)
    ville = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()

    class Meta:
        model = ResponsableEtablissement
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "adresse",
            "ville",
            "password",
            "numero_responsable",
            "type_responsable",
            "email",
        ]

    def create(self, validated_data):
        print(validated_data)
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        password = validated_data.pop("password")

        user = ResponsableEtablissement.objects.create_user(
            username=f"{first_name}.{last_name}".lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            numero_responsable=validated_data.get("numero_responsable", ""),
            type_responsable=validated_data.get("type_responsable", None),
            adresse=validated_data.get("adresse", ""),
            ville=validated_data.get("ville", ""),
            email=validated_data.get("email", ""),
        )

        return user


# Pour TypeCarteBancaire


class TypeCarteBancaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCarteBancaire
        fields = ("name", "regex_pattern")


class EditClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "username",
            "email",
            "numero_client",
            "ville",
            "adresse",
            "first_name",
            "last_name",
            "profilPic",
        ]

    def update(self, instance, validated_data):
        first_name = validated_data.get("first_name", instance.first_name.upper())
        last_name = validated_data.get("last_name", instance.last_name)
        instance.username = f"{first_name.upper()} {last_name}"
        instance.first_name = first_name
        instance.last_name = last_name
        instance.email = validated_data.get("email", instance.email)
        instance.numero_client = validated_data.get(
            "numero_client", instance.numero_client
        )
        instance.ville = validated_data.get("ville", instance.ville)
        instance.adresse = validated_data.get("adresse", instance.adresse)
        instance.profilPic = validated_data.get("profilPic", instance.profilPic)

        # Enregistrer les modifications
        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "username",
            "ban",
            "email",
            "numero_client",
            "numero_bancaire_client",
            "profilPic",
            "type_carte_bancaire",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "adresse",
            "ville",
        )

    extra_kwargs = {
        "password": {"write_only": True},
    }


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["ban"]


class ClientBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["ban"]


class AdminCheckSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["is_admin"]

    def get_is_admin(self, obj):
        return obj.is_superuser


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
