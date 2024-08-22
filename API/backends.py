from django.contrib.auth.backends import ModelBackend
from Accounts.models import Client, ResponsableEtablissement


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Client.objects.get(email=username)
        except Client.DoesNotExist:
            try:
                user = ResponsableEtablissement.objects.get(email=username)
            except ResponsableEtablissement.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None
