from django.db import models
from Accounts.models import ResponsableEtablissement, Client
from django.core.validators import MinValueValidator, MaxValueValidator


class TypeHebergement(models.Model):
    type_name = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.type_name


class HebergementImage(models.Model):
    hebergement = models.ForeignKey(
        "Hebergement", on_delete=models.CASCADE, related_name="images"
    )
    couverture = models.BooleanField(default=False)
    legende_hebergement = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images/images_Hebergement", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name


class Chambre(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_min_personnes = models.IntegerField(default=1)
    nombre_max_personnes = models.IntegerField(default=1)

    def __str__(self):
        return self.type_chambre


class ChambrePersonaliser(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_personnes = models.IntegerField(default=1)

    def __str__(self):
        return self.type_chambre


class TypeAccessoire(models.Model):
    nom_type = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_type


class AccessoireHebergement(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField(blank=True)
    type_accessoire = models.ForeignKey(
        TypeAccessoire, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_accessoire


class Hebergement(models.Model):
    nom_hebergement = models.CharField(max_length=100)
    description_hebergement = models.TextField(null=True, blank=True)
    nombre_etoile_hebergement = models.IntegerField(null=True, blank=True)
    responsable_hebergement = models.ForeignKey(
        ResponsableEtablissement, on_delete=models.CASCADE, related_name="hebergements"
    )
    type_hebergement = models.ForeignKey(
        TypeHebergement, null=True, on_delete=models.DO_NOTHING
    )
    nif = models.CharField(max_length=100, null=True, blank=True)
    stat = models.CharField(max_length=100, null=True, blank=True)
    autorisation = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Client, related_name="liked_hebergement", blank=True)
    taux_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=7.00,
        validators=[MinValueValidator(7.00), MaxValueValidator(15.00)],
    )

    def __str__(self):
        return self.nom_hebergement

    def total_likes(self):
        return self.likes.count()


class Localisation(models.Model):
    adresse = models.CharField(max_length=200, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    hebergement_id = models.OneToOneField(
        Hebergement,
        on_delete=models.CASCADE,
        related_name="localisation",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            str(self.id)
            + " "
            + str(self.hebergement_id.nom_hebergement if self.hebergement_id else "")
        )


class SocialLink(models.Model):
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name="social_link"
    )


class HebergementAccessoire(models.Model):
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name="accessoires"
    )
    accessoire = models.ForeignKey(AccessoireHebergement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hebergement.nom_hebergement} - {self.accessoire.nom_accessoire}"


class HebergementChambre(models.Model):
    nom_chambre = models.CharField(default=0, max_length=120)
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE)
    chambre = models.ForeignKey(
        Chambre, on_delete=models.CASCADE, null=True, blank=True
    )
    chambre_personaliser = models.ForeignKey(
        ChambrePersonaliser, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.CharField(max_length=2000, null=True, blank=True)
    superficie = models.IntegerField(null=True, blank=True)
    prix_nuit_chambre = models.DecimalField(max_digits=8, decimal_places=2)
    disponible_chambre = models.IntegerField(null=True, default=1)
    capacite = models.IntegerField(null=True)
    status = models.IntegerField(null=True, blank=True)
    accessoires = models.ManyToManyField(
        "AccessoireChambre", through="HebergementChambreAccessoire"
    )

    def prix_final(self):
        hebergement = self.hebergement
        taux_commission = hebergement.taux_commission / 100
        prix_final = self.prix_nuit_chambre * (1 + taux_commission)
        return prix_final

    def __str__(self):
        return f"{self.hebergement} - {self.chambre} - {self.chambre_personaliser}"


class AccessoireChambre(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_accessoire


class HebergementChambreAccessoire(models.Model):
    hebergement_chambre = models.ForeignKey(
        HebergementChambre, on_delete=models.CASCADE
    )
    accessoire_chambre = models.ForeignKey(AccessoireChambre, on_delete=models.CASCADE)

    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.hebergement_chambre} - {self.accessoire_chambre}"


class ImageChambre(models.Model):
    hebergement_chambre = models.ForeignKey(
        HebergementChambre, on_delete=models.CASCADE, related_name="images_chambre"
    )
    images = models.ImageField(upload_to="images/images_chambre")
    couverture = models.BooleanField(default=False)
    legende_chambre = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.images.name


# Reservation


class AvisClients(models.Model):
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name="avis_hotel"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="avis_client"
    )
    commentaire = models.CharField(null=True, max_length=500)
    note = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Note: {self.note} - Hebergement: {self.hebergement.nom_hebergement}"


class TransactionHebergement(models.Model):
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
        Client, on_delete=models.CASCADE, related_name="transactions"
    )

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"


class Reservation(models.Model):
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, related_name="reservations_hotel"
    )
    chambre_reserve = models.ForeignKey(
        HebergementChambre,
        on_delete=models.CASCADE,
        related_name="reservations_chambre",
    )
    client_reserve = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="reservations_client"
    )
    date_debut_reserve = models.DateField()
    date_fin_reserve = models.DateField()
    nombre_chambre_reserve = models.IntegerField(default=1)
    nombre_personnes_reserve = models.IntegerField(default=1)

    prix_total_reserve = models.DecimalField(max_digits=10, decimal_places=2)
    est_validee_reserve = models.BooleanField(default=False)
    transaction = models.ForeignKey(
        TransactionHebergement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f"{self.client_reserve} + {self.hebergement} + {self.est_validee_reserve}"
        )
