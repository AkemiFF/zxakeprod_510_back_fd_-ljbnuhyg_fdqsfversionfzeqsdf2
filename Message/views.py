from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import *

# HebergementMessage Views


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def hebergement_message_list_create(request):
    if request.method == 'GET':
        messages = HebergementMessage.objects.all()
        serializer = HebergementMessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HebergementMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def hebergement_message_detail(request, pk):
    try:
        message = HebergementMessage.objects.get(pk=pk)
    except HebergementMessage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HebergementMessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = HebergementMessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ArtisanatMessage Views


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def artisanat_message_list_create(request):
    if request.method == 'GET':
        messages = ArtisanatMessage.objects.all()
        serializer = ArtisanatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArtisanatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def artisanat_message_detail(request, pk):
    try:
        message = ArtisanatMessage.objects.get(pk=pk)
    except ArtisanatMessage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtisanatMessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ArtisanatMessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# TourOperateurMessage Views


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def tour_operateur_message_list_create(request):
    if request.method == 'GET':
        messages = TourOperateurMessage.objects.all()
        serializer = TourOperateurMessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TourOperateurMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def tour_operateur_message_detail(request, pk):
    try:
        message = TourOperateurMessage.objects.get(pk=pk)
    except TourOperateurMessage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TourOperateurMessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TourOperateurMessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
