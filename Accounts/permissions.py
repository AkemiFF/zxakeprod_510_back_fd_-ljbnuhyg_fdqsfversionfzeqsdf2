from rest_framework.permissions import BasePermission


class IsClientUser(BasePermission):
    """
    Permission qui permet uniquement aux utilisateurs du modèle Client d'accéder à la vue.
    """

    def has_permission(self, request, view):
        return bool(request.user)


# class IsResponsableHebergement(BasePermission):
#     """
#     Permet l'accès uniquement aux utilisateurs qui sont responsables d'un type 'Hebergement'.
#     """

#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False

#         return hasattr(request.user, 'type_responsable') and request.user.type_responsable.type_name == 'Hebergement'
