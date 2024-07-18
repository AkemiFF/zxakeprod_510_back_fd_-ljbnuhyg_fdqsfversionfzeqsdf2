from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.db.models.signals import pre_save
from django.dispatch import receiver
from Artisanal.models import *
from TourOperateur.models import *
from Hebergement.models import *

class Message(PolymorphicModel):
    sender = models.ForeignKey(
        Client, related_name='sent_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.get_receiver()}: {self.subject}"

    def get_receiver(self):
        raise NotImplementedError("Subclasses of Message must provide a get_receiver() method.")

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class HebergementMessage(Message):
    receiver = models.ForeignKey(
        Hebergement, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.subject}"

    def get_receiver(self):
        return self.receiver


class ArtisanatMessage(Message):
    artisanat = models.ForeignKey(
        Artisanat, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} -> {self.artisanat}: {self.subject}"

    def get_receiver(self):
        return self.artisanat


class TourOperateurMessage(Message):
    tour_operateur = models.ForeignKey(
        TourOperateur, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} -> {self.tour_operateur}: {self.subject}"

    def get_receiver(self):
        return self.tour_operateur


@receiver(pre_save, sender=HebergementMessage)
def check_reservation_before_save(sender, instance, **kwargs):
    client = instance.sender
    hebergement = instance.receiver

    if not Reservation.objects.filter(client_reserve=client, hotel_reserve=hebergement).exists():
        raise ValueError("Le client n'a pas effectué de réservation avec cet hébergement.")