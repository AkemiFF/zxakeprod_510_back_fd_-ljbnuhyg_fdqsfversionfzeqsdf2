# MyAccount/serialisers.py
from django.contrib.auth.models import User
from .models import Client
from rest_framework import serializers
from Accounts.models import *
from rest_framework import serializers


class UserSerializerVerify(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# Pour le TypeResponsable


class TypeResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeResponsable
        fields = '__all__'

# Pour ResponsableEtablissement


class ResponsableEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtablissement
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email',
            'numero_responsable', 'created_at', 'updated_at', 'type_responsable'
        )
        extra_kwargs = {
            'password_responsable': {'write_only': True},
        }

# Pour TypeCarteBancaire


class TypeCarteBancaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCarteBancaire
        fields = ('name', 'regex_pattern')

# Pour Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id', 'username', 'ban', 'email', 'numero_client', 'numero_bancaire_client',
            'type_carte_bancaire', 'created_at', 'updated_at', 'first_name', 'last_name', 'email', 'is_staff', 'is_active'
        )
    extra_kwargs = {
        'password': {'write_only': True},
    }


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['ban']


class ClientBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['ban']


class AdminCheckSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['is_admin']

    def get_is_admin(self, obj):
        return obj.is_superuser


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
