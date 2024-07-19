import json
from django.http import JsonResponse
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import *
from Accounts.permissions import *

# HebergementMessage Views
@api_view(['GET'])
@permission_classes([IsClientUser])
def get_messages_client_hebergement(request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            client_id = data['client_id']
            hebergement_id = data['hebergement_id']
            
            client = Client.objects.get(id=client_id)
            hebergement = Hebergement.objects.get(id=hebergement_id)
            
            messages = HebergementMessage.objects.filter(client=client,receiver=hebergement)
            dic_mess = dict()
            for i in messages:
                mess = {"content":i.content, 
                                           "client":i.client.id,
                                           "hebergment": i.receiver.id, 
                                           "client_is_sender": i.client_is_sender,
                                           "timestamp": i.timestamp,
                                           "subject": i.subject
                                    }
                dic_mess.setdefault(i.id,    mess)
              
                
            return JsonResponse({'messages': dic_mess}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    




#####################################################

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
