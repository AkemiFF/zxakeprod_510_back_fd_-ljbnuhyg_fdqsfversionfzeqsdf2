# views.py

from rest_framework import generics
from .serializers import ProduitArtisanalSerializer
from .models import ProduitArtisanal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from Artisanal.models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande
from Artisanal.serializers import ArtisanatSerializer, ProduitArtisanalSerializer, PanierSerializer, ItemPanierSerializer, CommandeSerializer


class ArtisanatListByResponsableView(generics.ListAPIView):
    serializer_class = ArtisanatSerializer

    def get_queryset(self):
        responsable_id = self.kwargs['responsable_id']
        return Artisanat.objects.filter(responsable_artisanat__id=responsable_id)


class ProduitArtisanalListByArtisanatView(generics.ListAPIView):
    serializer_class = ProduitArtisanalSerializer

    def get_queryset(self):
        artisanat_id = self.kwargs['artisanat_id']
        return ProduitArtisanal.objects.filter(artisanat__id=artisanat_id)


@api_view(['GET'])
def get_count_artisanat(request):
    try:
        number_artisanat = Artisanat.objects.count()
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_artisanat}, status=status.HTTP_200_OK)

# Visualiser tous les artisanal


@api_view(['GET'])
def get_all_artisanat(request):
    try:
        all_artisanat = Artisanat.objects.all()
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ArtisanatSerializer(all_artisanat, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser artisanal selon id


@api_view(['GET'])
def get_artisanat_by_id(request, pk):
    try:
        artisanat = Artisanat.objects.get(pk=pk)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ArtisanatSerializer(artisanat)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser artisanal selon id avec son responsable


@api_view(['GET'])
def get_artisanat_by_responsable_id(request, responsable_id):
    try:
        artisanat = Artisanat.objects.filter(
            responsable_artisanat=responsable_id)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ArtisanatSerializer(artisanat, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def artisanat_list_create(request):
    if request.method == 'GET':
        artisanats = Artisanat.objects.all()
        serializer = ArtisanatSerializer(artisanats, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtisanatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def artisanat_detail(request, pk):
    try:
        artisanat = Artisanat.objects.get(pk=pk)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtisanatSerializer(artisanat)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtisanatSerializer(artisanat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artisanat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ProduitArtisanal Views

# Nombre de produits artisanal créés


@api_view(['GET'])
def get_count_produit_artisanal(request):
    try:
        number_produit = ProduitArtisanal.objects.count()
    except ProduitArtisanal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_produit}, status=status.HTTP_200_OK)

# Visualiser tous les produits artisanal


@api_view(['GET'])
def get_all_produit_artisanal(request):
    try:
        all_produits = ProduitArtisanal.objects.all()
    except ProduitArtisanal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProduitArtisanalSerializer(all_produits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser produit artisanal selon id


@api_view(['GET'])
def get_produit_artisanal_by_id(request, pk):
    try:
        produit = ProduitArtisanal.objects.get(pk=pk)
    except ProduitArtisanal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProduitArtisanalSerializer(produit)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser produit artisanal selon id avec son responsable


@api_view(['GET'])
def get_produit_artisanal_by_responsable_id(request, responsable_id):
    try:
        produits = ProduitArtisanal.objects.filter(responsable=responsable_id)
    except ProduitArtisanal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProduitArtisanalSerializer(produits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def produit_artisanal_list_create(request):
    if request.method == 'GET':
        produits = ProduitArtisanal.objects.all()
        serializer = ProduitArtisanalSerializer(produits, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProduitArtisanalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def produit_artisanal_detail(request, pk):
    try:
        produit = ProduitArtisanal.objects.get(pk=pk)
    except ProduitArtisanal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProduitArtisanalSerializer(produit)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProduitArtisanalSerializer(produit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        produit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Panier Views

# Nombre de paniers créés


@api_view(['GET'])
def get_count_panier(request):
    try:
        number_panier = Panier.objects.count()
    except Panier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_panier}, status=status.HTTP_200_OK)

# Visualiser tous les paniers


@api_view(['GET'])
def get_all_panier(request):
    try:
        all_paniers = Panier.objects.all()
    except Panier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PanierSerializer(all_paniers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser panier selon id


@api_view(['GET'])
def get_panier_by_id(request, pk):
    try:
        panier = Panier.objects.get(pk=pk)
    except Panier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PanierSerializer(panier)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def panier_list_create(request):
    if request.method == 'GET':
        paniers = Panier.objects.all()
        serializer = PanierSerializer(paniers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PanierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def panier_detail(request, pk):
    try:
        panier = Panier.objects.get(pk=pk)
    except Panier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PanierSerializer(panier)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PanierSerializer(panier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        panier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ItemPanier Views

# Nombre d'items panier créés


@api_view(['GET'])
def get_count_item_panier(request):
    try:
        number_item_panier = ItemPanier.objects.count()
    except ItemPanier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_item_panier}, status=status.HTTP_200_OK)

# Visualiser tous les items panier


@api_view(['GET'])
def get_all_item_panier(request):
    try:
        all_items = ItemPanier.objects.all()
    except ItemPanier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ItemPanierSerializer(all_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser item panier selon id


@api_view(['GET'])
def get_item_panier_by_id(request, pk):
    try:
        item_panier = ItemPanier.objects.get(pk=pk)
    except ItemPanier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ItemPanierSerializer(item_panier)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def item_panier_list_create(request):
    if request.method == 'GET':
        items = ItemPanier.objects.all()
        serializer = ItemPanierSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ItemPanierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_panier_detail(request, pk):
    try:
        item = ItemPanier.objects.get(pk=pk)
    except ItemPanier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemPanierSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemPanierSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Commande Views

# Nombre de commandes créées


@api_view(['GET'])
def get_count_commande(request):
    try:
        number_commande = Commande.objects.count()
    except Commande.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_commande}, status=status.HTTP_200_OK)

# Visualiser toutes les commandes


@api_view(['GET'])
def get_all_commande(request):
    try:
        all_commandes = Commande.objects.all()
    except Commande.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CommandeSerializer(all_commandes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualiser commande selon id


@api_view(['GET'])
def get_commande_by_id(request, pk):
    try:
        commande = Commande.objects.get(pk=pk)
    except Commande.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CommandeSerializer(commande)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def commande_list_create(request):
    if request.method == 'GET':
        commandes = Commande.objects.all()
        serializer = CommandeSerializer(commandes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def commande_detail(request, pk):
    try:
        commande = Commande.objects.get(pk=pk)
    except Commande.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommandeSerializer(commande)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommandeSerializer(commande, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        commande.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
