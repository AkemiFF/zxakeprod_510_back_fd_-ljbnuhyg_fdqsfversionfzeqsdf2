from rest_framework import serializers

from Hebergement.models import Hebergement
from .models import Message, HebergementMessage

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'subject', 'content', 'timestamp']

class HebergementMessageSerializer(MessageSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=Hebergement.objects.all())

    class Meta:
        model = HebergementMessage
        fields = MessageSerializer.Meta.fields + ['receiver']
