from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsClient(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    emailproviderid = models.CharField(
        db_column="emailProviderId", max_length=80, blank=True, null=True
    )  # Field name made lowercase.
    emailprovideruid = models.CharField(
        db_column="emailProviderUid", max_length=80, blank=True, null=True
    )  # Field name made lowercase.
    emailphotourl = models.CharField(
        db_column="emailPhotoUrl", max_length=280, blank=True, null=True
    )  # Field name made lowercase.
    ban = models.BooleanField()
    email = models.CharField(unique=True, max_length=254)
    numero_client = models.CharField(max_length=10)
    numero_bancaire_client = models.CharField(max_length=19, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type_carte_bancaire = models.ForeignKey(
        "AccountsTypecartebancaire", models.DO_NOTHING, blank=True, null=True
    )
    profilpic = models.CharField(
        db_column="profilPic", max_length=100, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Accounts_client"


class AccountsClientGroups(models.Model):
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    group = models.ForeignKey("AuthGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Accounts_client_groups"
        unique_together = (("client", "group"),)


class AccountsClientUserPermissions(models.Model):
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Accounts_client_user_permissions"
        unique_together = (("client", "permission"),)


class AccountsResponsableetablissement(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    numero_responsable = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type_responsable = models.ForeignKey(
        "AccountsTyperesponsable", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Accounts_responsableetablissement"


class AccountsResponsableetablissementGroups(models.Model):
    responsableetablissement = models.ForeignKey(
        AccountsResponsableetablissement, models.DO_NOTHING
    )
    group = models.ForeignKey("AuthGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Accounts_responsableetablissement_groups"
        unique_together = (("responsableetablissement", "group"),)


class AccountsResponsableetablissementUserPermissions(models.Model):
    responsableetablissement = models.ForeignKey(
        AccountsResponsableetablissement, models.DO_NOTHING
    )
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Accounts_responsableetablissement_user_permissions"
        unique_together = (("responsableetablissement", "permission"),)


class AccountsTypecartebancaire(models.Model):
    name = models.CharField(unique=True, max_length=50)
    regex_pattern = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "Accounts_typecartebancaire"


class AccountsTyperesponsable(models.Model):
    type_name = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Accounts_typeresponsable"


class AccountsVerificationcode(models.Model):
    user_email = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    used = models.BooleanField()

    class Meta:
        managed = False
        db_table = "Accounts_verificationcode"


class ArtisanalArtisanat(models.Model):
    localisation = models.ForeignKey("HebergementLocalisation", models.DO_NOTHING)
    responsable_artisanat = models.ForeignKey(
        AccountsResponsableetablissement, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "Artisanal_artisanat"


class ArtisanalCommande(models.Model):
    prix_total = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    date_commande = models.DateTimeField()
    status = models.CharField(max_length=20)
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    panier = models.OneToOneField(
        "ArtisanalPanier", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Artisanal_commande"


class ArtisanalItempanier(models.Model):
    quantite = models.PositiveIntegerField()
    panier = models.ForeignKey("ArtisanalPanier", models.DO_NOTHING)
    produit = models.ForeignKey("ArtisanalProduitartisanal", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Artisanal_itempanier"


class ArtisanalPanier(models.Model):
    total = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    client = models.OneToOneField(AccountsClient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Artisanal_panier"


class ArtisanalProduitartisanal(models.Model):
    nom_produit_artisanal = models.CharField(max_length=100)
    description_artisanat = models.TextField()
    prix_artisanat = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    disponible_artisanat = models.BooleanField()
    image_artisanat = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    artisanat = models.ForeignKey(
        ArtisanalArtisanat, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Artisanal_produitartisanal"


class HebergementAccessoirechambre(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "Hebergement_accessoirechambre"


class HebergementAccessoirehebergement(models.Model):
    nom_accessoire = models.CharField(max_length=100)
    description_accessoire = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type_accessoire = models.ForeignKey(
        "HebergementTypeaccessoire", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Hebergement_accessoirehebergement"


class HebergementAvisclients(models.Model):
    commentaire = models.CharField(max_length=500, blank=True, null=True)
    note = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    hebergement = models.ForeignKey("HebergementHebergement", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Hebergement_avisclients"


class HebergementChambre(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_min_personnes = models.IntegerField()
    nombre_max_personnes = models.IntegerField()

    class Meta:
        managed = False
        db_table = "Hebergement_chambre"


class HebergementChambrepersonaliser(models.Model):
    type_chambre = models.CharField(max_length=100)
    nombre_personnes = models.IntegerField()

    class Meta:
        managed = False
        db_table = "Hebergement_chambrepersonaliser"


class HebergementHebergement(models.Model):
    nom_hebergement = models.CharField(max_length=100)
    description_hebergement = models.TextField()
    nombre_etoile_hebergement = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    responsable_hebergement = models.ForeignKey(
        AccountsResponsableetablissement, models.DO_NOTHING
    )
    type_hebergement = models.ForeignKey(
        "HebergementTypehebergement", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Hebergement_hebergement"


class HebergementHebergementaccessoire(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    accessoire = models.ForeignKey(HebergementAccessoirehebergement, models.DO_NOTHING)
    hebergement = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Hebergement_hebergementaccessoire"


class HebergementHebergementchambre(models.Model):
    prix_nuit_chambre = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    disponible_chambre = models.IntegerField(blank=True, null=True)
    chambre = models.ForeignKey(
        HebergementChambre, models.DO_NOTHING, blank=True, null=True
    )
    chambre_personaliser = models.ForeignKey(
        HebergementChambrepersonaliser, models.DO_NOTHING, blank=True, null=True
    )
    hebergement = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)
    description = models.CharField(max_length=300, blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Hebergement_hebergementchambre"


class HebergementHebergementchambreaccessoire(models.Model):
    note = models.CharField(max_length=255, blank=True, null=True)
    accessoire_chambre = models.ForeignKey(
        HebergementAccessoirechambre, models.DO_NOTHING
    )
    hebergement_chambre = models.ForeignKey(
        HebergementHebergementchambre, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "Hebergement_hebergementchambreaccessoire"


class HebergementHebergementimage(models.Model):
    couverture = models.BooleanField()
    legende_hebergement = models.CharField(max_length=200)
    image = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hebergement = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Hebergement_hebergementimage"


class HebergementHebergementlike(models.Model):
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    hebergement = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Hebergement_hebergementlike"
        unique_together = (("hebergement", "client"),)


class HebergementImagechambre(models.Model):
    images = models.CharField(max_length=100)
    couverture = models.BooleanField()
    legende_chambre = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hebergement_chambre = models.ForeignKey(
        HebergementHebergementchambre, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "Hebergement_imagechambre"


class HebergementLocalisation(models.Model):
    adresse = models.CharField(max_length=200, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    hebergement_id = models.OneToOneField(
        HebergementHebergement, models.DO_NOTHING, blank=True, null=True
    )

    # composer, IntelliCode
    class Meta:
        managed = False
        db_table = "Hebergement_localisation"


class HebergementReservation(models.Model):
    date_debut_reserve = models.DateField()
    date_fin_reserve = models.DateField()
    nombre_personnes_reserve = models.IntegerField()
    prix_total_reserve = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    est_validee_reserve = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    chambre_reserve = models.ForeignKey(
        HebergementHebergementchambre, models.DO_NOTHING
    )
    client_reserve = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    hotel_reserve = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Hebergement_reservation"


class HebergementTypeaccessoire(models.Model):
    nom_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "Hebergement_typeaccessoire"


class HebergementTypehebergement(models.Model):
    type_name = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Hebergement_typehebergement"


class MessageArtisanatmessage(models.Model):
    message_ptr = models.OneToOneField(
        "MessageMessage", models.DO_NOTHING, primary_key=True
    )
    receiver = models.ForeignKey(ArtisanalArtisanat, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Message_artisanatmessage"


class MessageHebergementmessage(models.Model):
    message_ptr = models.OneToOneField(
        "MessageMessage", models.DO_NOTHING, primary_key=True
    )
    receiver = models.ForeignKey(HebergementHebergement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Message_hebergementmessage"


class MessageMessage(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField()
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    client_is_sender = models.BooleanField()
    subject = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Message_message"


class MessageTouroperateurmessage(models.Model):
    message_ptr = models.OneToOneField(
        MessageMessage, models.DO_NOTHING, primary_key=True
    )
    receiver = models.ForeignKey("TouroperateurTouroperateur", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Message_touroperateurmessage"


class TouroperateurAvistouroperateur(models.Model):
    note = models.PositiveIntegerField()
    commentaire = models.TextField(blank=True, null=True)
    date_avis = models.DateTimeField()
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    tour_operateur = models.ForeignKey("TouroperateurTouroperateur", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "TourOperateur_avistouroperateur"


class TouroperateurImagetour(models.Model):
    image = models.CharField(max_length=100)
    couverture = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    images_tour = models.ForeignKey("TouroperateurTouroperateur", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "TourOperateur_imagetour"


class TouroperateurImagevoyage(models.Model):
    couverture = models.BooleanField()
    image_voyage = models.ForeignKey(
        "TouroperateurVoyage", models.DO_NOTHING, blank=True, null=True
    )
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TourOperateur_imagevoyage"


class TouroperateurInclusionvoyage(models.Model):
    voyage = models.ForeignKey(
        "TouroperateurVoyage", models.DO_NOTHING, blank=True, null=True
    )
    type_inclusion = models.ForeignKey(
        "TouroperateurTypeinclusion", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TourOperateur_inclusionvoyage"


class TouroperateurReservationVoyage(models.Model):
    date_reservation_voyage = models.DateTimeField()
    status = models.CharField(max_length=20)
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    voyage = models.ForeignKey("TouroperateurVoyage", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "TourOperateur_reservation_voyage"


class TouroperateurSatisfactionclient(models.Model):
    est_satisfait = models.BooleanField()
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    tour = models.ForeignKey("TouroperateurTouroperateur", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "TourOperateur_satisfactionclient"
        unique_together = (("client", "tour"),)


class TouroperateurTouroperateur(models.Model):
    nom_operateur = models.CharField(max_length=100)
    adresse_operateur = models.CharField(max_length=255, blank=True, null=True)
    email_operateur = models.CharField(
        unique=True, max_length=254, blank=True, null=True
    )
    description_operateur = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    responsable_touroperateur = models.ForeignKey(
        AccountsResponsableetablissement,
        models.DO_NOTHING,
        db_column="responsable_TourOperateur_id",
    )  # Field name made lowercase.
    telephone_operateur = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TourOperateur_touroperateur"


class TouroperateurTrajetvoyage(models.Model):
    numero_trajet = models.IntegerField(blank=True, null=True)
    date_trajet = models.DateField(blank=True, null=True)
    voyage = models.ForeignKey("TouroperateurVoyage", models.DO_NOTHING)
    nom_ville = models.CharField(max_length=250, blank=True, null=True)
    description_trajet = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TourOperateur_trajetvoyage"


class TouroperateurTypeinclusion(models.Model):
    nom_inclusion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TourOperateur_typeinclusion"


class TouroperateurTypetransport(models.Model):
    nom_type = models.CharField(max_length=100)
    place = models.IntegerField()

    class Meta:
        managed = False
        db_table = "TourOperateur_typetransport"


class TouroperateurVoyage(models.Model):
    nom_voyage = models.CharField(max_length=100)
    description_voyage = models.TextField()
    destination_voyage = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix_voyage = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    places_disponibles = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tour_operateur = models.ForeignKey(TouroperateurTouroperateur, models.DO_NOTHING)
    type_transport = models.ForeignKey(
        TouroperateurTypetransport, models.DO_NOTHING, blank=True, null=True
    )
    ville_depart = models.CharField(max_length=100)
    distance = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TourOperateur_voyage"


class TouroperateurVoyagelike(models.Model):
    client = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    voyage = models.ForeignKey(TouroperateurVoyage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "TourOperateur_voyagelike"
        unique_together = (("voyage", "client"),)


class AccountEmailaddress(models.Model):
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = "account_emailaddress"
        unique_together = (
            ("user", "primary"),
            ("user", "email"),
        )


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "account_emailconfirmation"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=200)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    user = models.ForeignKey(AccountsClient, models.DO_NOTHING)
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = "socialaccount_socialaccount"
        unique_together = (("provider", "uid"),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    provider_id = models.CharField(max_length=200)
    settings = models.JSONField()

    class Meta:
        managed = False
        db_table = "socialaccount_socialapp"


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(
        SocialaccountSocialapp, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "socialaccount_socialtoken"
        unique_together = (("app", "account"),)
