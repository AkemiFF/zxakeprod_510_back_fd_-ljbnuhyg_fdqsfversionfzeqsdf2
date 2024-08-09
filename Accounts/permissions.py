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


class IsClientOrRelatedToHebergement(BasePermission):
    def has_permission(self, request, view):
        try:
            data = json.loads(request.body.decode("utf-8"))
            client_id = data.get("client_id")
            hebergement_id = data.get("hebergement_id")

            if request.user.is_authenticated:
                if (
                    client_id
                    and Client.objects.filter(id=client_id, user=request.user).exists()
                ):
                    return True
                if (
                    hebergement_id
                    and Hebergement.objects.filter(
                        id=hebergement_id, related_user=request.user
                    ).exists()
                ):
                    return True
        except Exception:
            return False
        return False


class IsResponsableEtablissement(BasePermission):
    """
    Permission qui autorise uniquement les ResponsablesEtablissement.
    """

    def has_permission(self, request, view):
        return request.user and isinstance(request.user, ResponsableEtablissement)
