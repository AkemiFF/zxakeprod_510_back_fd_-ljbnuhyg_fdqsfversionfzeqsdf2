from django.db import models
from django.contrib.auth.models import User
from Artisanal.models import *
from Hebergement.models import *
from polymorphic.models import PolymorphicModel


class Message(PolymorphicModel):
    sender = models.ForeignKey(
        Client, related_name='sent_messages', on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.sender} -> {self.receiver}: {self.subject}"


class HebergementMessage(Message):
    receiver = models.ForeignKey(
        Hebergement, related_name='messages', on_delete=models.CASCADE)

# class ArtisanatMessage(Message):
#     artisanat = models.ForeignKey(
#         Artisanat, related_name='messages', on_delete=models.CASCADE)


# class TourOperateurMessage(Message):
#     tour_operateur = models.ForeignKey(
#         TourOperateur, related_name='messages', on_delete=models.CASCADE)
