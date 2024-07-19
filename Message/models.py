from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.db.models.signals import pre_save
from django.dispatch import receiver
from Artisanal.models import *
from TourOperateur.models import *
from Hebergement.models import *
from django.conf import settings



class Message(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)  # Utilisation de settings.AUTH_USER_MODEL
    content = models.TextField()
    subject = models.CharField(max_length=255, default='', null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    client_is_sender = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.client} -> {self.get_receiver()}: {self.content}"

    def get_receiver(self):
        raise NotImplementedError("Subclasses of Message must provide a get_receiver() method.")

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class HebergementMessage(Message):
    receiver = models.ForeignKey(
        Hebergement, related_name='messages', on_delete=models.CASCADE)
    
    def __str__(self):
        if self.client_is_sender:
            return f"{self.client} -> {self.receiver}: {self.content}"
        else:
            return f"{self.receiver} -> {self.client}: {self.content}"

    def get_receiver(self):
        return self.receiver


class ArtisanatMessage(Message):
    receiver = models.ForeignKey(
        Artisanat, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        if self.client_is_sender:
            return f"{self.client} -> {self.receiver}: {self.content}"
        else:
            return f"{self.receiver} -> {self.client}: {self.content}"

    def get_receiver(self):
        return self.receiver


class TourOperateurMessage(Message):
    receiver = models.ForeignKey(
        TourOperateur, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        if self.client_is_sender:
            return f"{self.client} -> {self.receiver}: {self.content}"
        else:
            return f"{self.receiver} -> {self.client}: {self.content}"

    def get_receiver(self):
        return self.receiver


@receiver(pre_save, sender=HebergementMessage)
def check_reservation_before_save(sender, instance, **kwargs): 
    client = instance.client
    hebergement = instance.receiver

    if not Reservation.objects.filter(client_reserve=client, hotel_reserve=hebergement).exists():
        raise ValueError("Le client n'a pas effectué de réservation avec cet hébergement.")
