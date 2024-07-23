from django.contrib import admin
from .models import *


admin.site.register(Hebergement)
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
admin.site.register(HebergementLike)
