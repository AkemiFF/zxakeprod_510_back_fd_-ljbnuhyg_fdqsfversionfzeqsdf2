from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TourOperateur)
admin.site.register(Voyage)
admin.site.register(ImageVoyage)
admin.site.register(Reservation_voyage)

