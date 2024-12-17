from Accounts.models import Client, ResponsableEtablissement
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user = ResponsableEtablissement.objects.get(
                    id=validated_token["user_id"]
                )
        except Client.DoesNotExist:
            try:
                user = ResponsableEtablissement.objects.get(
                    id=validated_token["user_id"]
                )
            except ResponsableEtablissement.DoesNotExist:
                raise AuthenticationFailed(
                    "Utilisateur non trouvé.", code="user_not_found"
                )

        return user
