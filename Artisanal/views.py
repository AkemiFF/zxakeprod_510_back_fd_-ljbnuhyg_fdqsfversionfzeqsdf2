from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArtisanatSerializer, ProduitArtisanalSerializer, PanierSerializer, ItemPanierSerializer, CommandeSerializer
from Artisanal.models import Artisanat, ProduitArtisanal, Panier,ItemPanier, Commande 
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsClientUser


# Pour la partie Artisanal
@api_view(['GET'])
def artisanal_get(request ,pk):
    try:
        artisanal = Artisanat.objects.get(pk=pk)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArtisanatSerializer(artisanal)
    return Response(serializer.data)

@api_view(['POST'])
def artisanal_post(request):
    serializer = ArtisanatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def artisanal_put(request, pk):
    try:
        artisanal = Artisanat.objects.get(pk=pk)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArtisanatSerializer(artisanal, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def aritisanal_delete(request, pk):
    try:
        artisanal = Artisanat.objects.get(pk=pk)
    except Artisanat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    artisanal.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Pour la partie ProduitArtisanal
@api_view(['GET'])
def 
