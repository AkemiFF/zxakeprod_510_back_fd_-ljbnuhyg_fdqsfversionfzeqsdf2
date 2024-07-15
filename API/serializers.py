from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "No active account found with the given credentials"
                )

            if not user.check_password(password):
                raise serializers.ValidationError(
                    "No active account found with the given credentials"
                )

            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")

            data = super().validate(attrs)

            # Ne pas inclure 'username' dans les données validées
            if 'username' in data:
                del data['username']

            data['user'] = user
            return data
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajoutez les revendications supplémentaires ici, si nécessaire
        return token
