from rest_framework import viewsets, permissions
from .models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande
from .serializers import (
    ArtisanatSerializer, ProduitArtisanalSerializer, PanierSerializer,
    ItemPanierSerializer, CommandeSerializer
)

class ArtisanatViewSet(viewsets.ModelViewSet):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class ProduitArtisanalViewSet(viewsets.ModelViewSet):
    queryset = ProduitArtisanal.objects.all()
    serializer_class = ProduitArtisanalSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class ItemPanierViewSet(viewsets.ModelViewSet):
    queryset = ItemPanier.objects.all()
    serializer_class = ItemPanierSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed
