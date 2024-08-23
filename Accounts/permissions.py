import json
from rest_framework.permissions import BasePermission

from .models import *
from Hebergement.models import *


class IsClientUser(BasePermission):
    """
    Permission qui permet uniquement aux utilisateurs du modèle Client d'accéder à la vue.
    """

    def has_permission(self, request, view):
        return bool(request.user)


class IsResponsable(BasePermission):
    """
    Permission qui permet l'accès uniquement aux utilisateurs du modèle ResponsableEtablissement.
    """

    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et s'il est du modèle ResponsableEtablissement
        return request.user and hasattr(request.user, "type_responsable")
