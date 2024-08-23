from django.db import models
from Accounts.models import ResponsableEtablissement, Client
from django.utils.translation import gettext_lazy as _


class TypeInclusion(models.Model):
    nom_inclusion = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.nom_inclusion

    class Meta:
        verbose_name = "Type d'Inclusion"
        verbose_name_plural = "Types d'Inclusion"


class TourOperateur(models.Model):
    nom_operateur = models.CharField(max_length=100)
    responsable_TourOperateur = models.ForeignKey(
        ResponsableEtablissement, on_delete=models.CASCADE, related_name="tourOperateur"
    )
    adresse_operateur = models.CharField(max_length=255, null=True, blank=True)
    email_operateur = models.EmailField(unique=True, null=True, blank=True)
    telephone_operateur = models.CharField(max_length=10, null=True, blank=True)
    description_operateur = models.TextField(blank=True, null=True)
    stat = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_operateur

    class Meta:
        verbose_name = "Tour Operateur"
        verbose_name_plural = "Tour Operateurs"


class LocalisationTour(models.Model):
    adresse = models.CharField(max_length=200, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tour_id = models.OneToOneField(
        TourOperateur,
        on_delete=models.CASCADE,
        related_name="localisation_tour",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.adresse


class AvisTourOperateur(models.Model):
    tour_operateur = models.ForeignKey(
        TourOperateur, on_delete=models.CASCADE, related_name="avis_tour_operateur"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    note = models.PositiveIntegerField()  # Par exemple, sur 5 ou 10
    commentaire = models.TextField(blank=True, null=True)
    date_avis = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis Tour Operateur"
        verbose_name_plural = "Avis Tour Operateurs"
        ordering = ["-date_avis"]

    def __str__(self):
        return f"Avis de {self.client} pour {self.tour_operateur} - {self.note} étoiles"


class TypeTransport(models.Model):
    nom_type = models.CharField(max_length=100)
    place = models.IntegerField(default=12)

    def __str__(self) -> str:
        return self.nom_type

    class Meta:
        verbose_name = "Type de Transport"
        verbose_name_plural = "Types de Transport"


class ImageTour(models.Model):
    images_tour = models.ForeignKey(
        TourOperateur, on_delete=models.CASCADE, related_name="images_tour"
    )
    image = models.ImageField(upload_to="images/images_tour")
    couverture = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.image.name} for {self.images_tour}"

    class Meta:
        verbose_name = "Image Tour"
        verbose_name_plural = "Images Tour"


class InclusionVoyage(models.Model):
    type_inclusion = models.ForeignKey(
        TypeInclusion,
        on_delete=models.CASCADE,
        related_name="voyage_part",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.type_inclusion}"

    class Meta:
        verbose_name = "Inclusion Voyage"
        verbose_name_plural = "Inclusions Voyage"


class Voyage(models.Model):
    tour_operateur = models.ForeignKey(
        TourOperateur, on_delete=models.CASCADE, related_name="voyages"
    )
    nom_voyage = models.CharField(max_length=100)
    ville_depart = models.CharField(max_length=100, default="Antananarivo")
    destination_voyage = models.CharField(max_length=255)
    description_voyage = models.TextField()

    date_debut = models.DateField()
    date_fin = models.DateField()

    distance = models.IntegerField(null=True)

    prix_voyage = models.DecimalField(max_digits=10, decimal_places=2)
    places_disponibles = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inclusions = models.ManyToManyField(
        TypeInclusion, related_name="voyages", blank=True
    )

    type_transport = models.ForeignKey(
        TypeTransport,
        on_delete=models.DO_NOTHING,
        related_name="type_transport",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nom_voyage

    @property
    def nb_like(self):
        return self.likes.count()

    def get_couverture_images(self):
        return self.images_voyage.filter(couverture=True)

    class Meta:
        verbose_name = "Voyage"
        verbose_name_plural = "Voyages"


class TrajetVoyage(models.Model):
    numero_trajet = models.IntegerField(null=True, blank=True)
    voyage = models.ForeignKey(
        Voyage, on_delete=models.CASCADE, related_name="voyage_trajet"
    )
    nom_ville = models.CharField(max_length=250, null=True)
    date_trajet = models.DateField(null=True, blank=True)
    description_trajet = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.voyage.nom_voyage} - {self.numero_trajet}"


class SatisfactionClient(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_satisfaction", null=False
    )
    tour = models.ForeignKey(
        TourOperateur,
        on_delete=models.CASCADE,
        related_name="tour_satisfaction",
        null=False,
    )
    est_satisfait = models.BooleanField(default=False)

    class Meta:
        unique_together = ("client", "tour")
        verbose_name = "Satisfaction Client"
        verbose_name_plural = "Satisfactions Clients"

    def __str__(self):
        return f"{self.client} satisfaction with {self.tour} is {self.est_satisfait}"


class VoyageLike(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, related_name="likes")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("voyage", "client")
        verbose_name = "Voyage Like"
        verbose_name_plural = "Voyage Likes"

    def __str__(self):
        return f"{self.client} likes {self.voyage}"


class ImageVoyage(models.Model):
    image_voyage = models.ForeignKey(
        Voyage,
        on_delete=models.CASCADE,
        related_name="images_voyage",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images/images_voyage", null=True, blank=True)
    couverture = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.image.name} for {self.image_voyage}"

    class Meta:
        verbose_name = "Image Voyage"
        verbose_name_plural = "Images Voyage"


class TransactionTour(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payer_name = models.CharField(max_length=255)
    payer_email = models.EmailField()
    payer_id = models.CharField(max_length=255)
    payee_email = models.EmailField()
    merchant_id = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=10, null=True, blank=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    capture_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="transactions_tour"
    )

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"


class ReservationVoyage(models.Model):
    voyage = models.ForeignKey(
        Voyage, on_delete=models.CASCADE, related_name="reservations_voyage"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    transaction = models.ForeignKey(
        TransactionTour, on_delete=models.CASCADE, null=True, blank=True
    )
    date_reservation_voyage = models.DateTimeField(auto_now_add=True)
    nombre_voyageurs = models.IntegerField(default=1)
    prix_total = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} reserved {self.voyage}"

    class Meta:
        verbose_name = "Reservation Voyage"
        verbose_name_plural = "Reservations Voyage"


# class TrajetVoyage(models.Model):
#     numero_trajet = models.IntegerField(null=True, blank=True)
#     voyage = models.ForeignKey(
#         Voyage, on_delete=models.CASCADE, related_name="voyage_trajet"
#     )
#     nom_ville = models.CharField(max_length=250, null=True)
#     date_trajet = models.DateField(null=True, blank=True)
#     description_trajet = models.CharField(max_length=1000, null=True, blank=True)

#     def __str__(self) -> str:
#         return f"{self.voyage.nom_voyage} - {self.numero_trajet}"
