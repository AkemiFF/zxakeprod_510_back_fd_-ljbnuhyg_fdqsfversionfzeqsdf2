from django.db import models
from Accounts.models import ResponsableEtablissement
from Accounts.models import Client
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TourOperateur(models.Model):
    nom_operateur = models.CharField(max_length=100)
    responsable_TourOperateur = models.ForeignKey(ResponsableEtablissement, on_delete=models.CASCADE, related_name='tourOperateur')
    adresse_operateur = models.CharField(max_length=255)
    email_operateur = models.EmailField(unique=True)
    telephone_operateur = models.CharField(max_length=10, validators=[RegexValidator(
        regex=r'^(032|033|034|038)\d{7}$', message='Le numéro doit commencer par 032, 033, 034 ou 038 et contenir 7 chiffres supplémentaires.')])
    description_operateur = models.TextField(blank=True, null=True)
    image_tour = models.ImageField(upload_to='images/Tour_operateur', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_operateur

class Voyage(models.Model):
    tour_operateur = models.ForeignKey(TourOperateur, on_delete=models.CASCADE, related_name='voyages')
    nom_voyage = models.CharField(max_length=100)
    description_voyage = models.TextField()
    destination_voyage = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix_voyage = models.DecimalField(max_digits=10, decimal_places=2)
    places_disponibles = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_voyage
    
class ImageVoyage(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/Touroperateur_voyage')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.voyage.nom_voyage}"

class Reservation_voyage(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_reservation_voyage = models.DateTimeField(auto_now_add=True)
    
    # Choices for reservation status
    STATUS_CHOICES = (
        ('confirmed', _('Confirmée')),
        ('pending', _('En attente')),
        ('cancelled', _('Annulée')),
        # Add more statuses as needed
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')