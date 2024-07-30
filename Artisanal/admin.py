from django.contrib import admin
from Artisanal.models import *


class ProduitArtisanalAdmin(admin.ModelAdmin):
    list_display = (
        "nom_produit_artisanal",
        "prix_artisanat",
        "disponible_artisanat",
        "artisanat",
    )
    filter_horizontal = ("specifications",)


admin.site.register(ProduitArtisanal, ProduitArtisanalAdmin)

admin.site.register(AvisClientProduitArtisanal)
admin.site.register(Specification)
admin.site.register(Artisanat)
admin.site.register(LocalisationArtisanat)
admin.site.register(ImageProduitArtisanal)


admin.site.register(Panier)
admin.site.register(ItemPanier)
admin.site.register(Commande)
