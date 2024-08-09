from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TourOperateur)
admin.site.register(Voyage)
admin.site.register(VoyageLike)
admin.site.register(TypeInclusion)
admin.site.register(InclusionVoyage)
admin.site.register(ImageVoyage)
admin.site.register(LocalisationTour)
admin.site.register(TypeTransport)
admin.site.register(ImageTour)
admin.site.register(TrajetVoyage)
admin.site.register(ReservationVoyage)
admin.site.register(AvisTourOperateur)
