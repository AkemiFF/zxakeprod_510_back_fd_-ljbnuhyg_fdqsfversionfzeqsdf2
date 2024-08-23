from django.contrib import admin
from .models import *


class TransactionHebergementAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "status",
        "amount_formatted",
        "currency",
        "payer_name",
        "payer_email",
        "payee_email",
        "description",
        "create_time_formatted",
        "update_time_formatted",
    )
    search_fields = ("transaction_id", "payer_name", "payer_email")
    list_filter = ("status", "currency", "create_time")

    def amount_formatted(self, obj):
        return f"{obj.amount} {obj.currency}"

    amount_formatted.short_description = "Amount"

    def create_time_formatted(self, obj):
        return obj.create_time.strftime("%Y-%m-%d %H:%M:%S")

    create_time_formatted.short_description = "Created At"

    def update_time_formatted(self, obj):
        return obj.update_time.strftime("%Y-%m-%d %H:%M:%S")

    update_time_formatted.short_description = "Updated At"


# Enregistrez le modèle avec la classe d'administration personnalisée
admin.site.register(TransactionHebergement, TransactionHebergementAdmin)


@admin.register(Hebergement)
class HebergementAdmin(admin.ModelAdmin):
    list_display = ["nom_hebergement", "taux_commission"]
    fields = [
        "nom_hebergement",
        "description_hebergement",
        "nombre_etoile_hebergement",
        "responsable_hebergement",
        "type_hebergement",
        "nif",
        "stat",
        "autorisation",
        "delete",
        "taux_commission",
        "likes",
    ]


admin.site.register(HebergementImage)

admin.site.register(AccessoireHebergement)
admin.site.register(HebergementAccessoire)

admin.site.register(HebergementChambreAccessoire)
admin.site.register(HebergementChambre)
admin.site.register(Chambre)
admin.site.register(ChambrePersonaliser)
admin.site.register(AccessoireChambre)
admin.site.register(ImageChambre)
admin.site.register(Localisation)


admin.site.register(TypeHebergement)

admin.site.register(Reservation)
admin.site.register(AvisClients)
admin.site.register(TypeAccessoire)
# admin.site.register(HebergementLike)
