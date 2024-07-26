from rest_framework import viewsets, permissions, generics, status
from .models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ArtisanatViewSet(viewsets.ModelViewSet):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatDetailSerializer
    permission_classes = [permissions.AllowAny]


class ProduitArtisanalViewSet(viewsets.ModelViewSet):
    queryset = ProduitArtisanal.objects.all()
    serializer_class = ProduitArtisanalSerializer
    permission_classes = [permissions.AllowAny]


class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [permissions.AllowAny]


class ItemPanierViewSet(viewsets.ModelViewSet):
    queryset = ItemPanier.objects.all()
    serializer_class = ItemPanierSerializer
    permission_classes = [permissions.AllowAny]


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.AllowAny]


class ProduitArtisanalDetailView(generics.RetrieveAPIView):
    queryset = ProduitArtisanal.objects.all()
    serializer_class = ProduitArtisanalDetailSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["POST"])
def like_produit(request, produit_id):
    try:
        produit = ProduitArtisanal.objects.get(id=produit_id)
    except ProduitArtisanal.DoesNotExist:
        return Response(
            {"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user
    if user in produit.likes.all():
        produit.likes.remove(user)
        return Response({"message": "Like retiré"}, status=status.HTTP_200_OK)
    else:
        produit.likes.add(user)
        return Response({"message": "Like ajouté"}, status=status.HTTP_200_OK)
