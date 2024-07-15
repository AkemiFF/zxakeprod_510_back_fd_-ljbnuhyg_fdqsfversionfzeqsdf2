from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Message, HebergementMessage
from .serializers import MessageSerializer, HebergementMessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class HebergementMessageListCreateView(generics.ListCreateAPIView):
    queryset = HebergementMessage.objects.all()
    serializer_class = HebergementMessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class HebergementMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HebergementMessage.objects.all()
    serializer_class = HebergementMessageSerializer
