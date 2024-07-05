from django.db.models.signals import post_migrate
from django.dispatch import receiver
import Accounts
from Accounts.models import TypeCarteBancaire, TypeResponsable


@receiver(post_migrate)
def create_initial_types(sender, **kwargs):
    if sender.name == 'Accounts':
        TypeResponsable.objects.get_or_create(type_name="Hebergement")
        TypeResponsable.objects.get_or_create(type_name="Artisanal")
        TypeResponsable.objects.get_or_create(type_name="Tour Operateur")

        TypeCarteBancaire.objects.get_or_create(
            name="VISA", regex_pattern=r'^4[0-9]{12}(?:[0-9]{3})?$')
        TypeCarteBancaire.objects.get_or_create(
            name="MasterCard", regex_pattern=r'^5[1-5][0-9]{14}$')
        TypeCarteBancaire.objects.get_or_create(
            name="American Express", regex_pattern=r'^3[47][0-9]{13}$')
        TypeCarteBancaire.objects.get_or_create(
            name="Discover", regex_pattern=r'^6(?:011|5[0-9]{2})[0-9]{12}$')
        TypeCarteBancaire.objects.get_or_create(
            name="JCB", regex_pattern=r'^(?:2131|1800|35\d{3})\d{11}$')
        TypeCarteBancaire.objects.get_or_create(
            name="Visa Electron", regex_pattern=r'^(4026|417500|4405|4508|4844|4913|4917)\d{10}$')
        TypeCarteBancaire.objects.get_or_create(
            name="Maestro", regex_pattern=r'^(5018|5020|5038|6304|6759|6761|6763)\d{8,15}$')
        TypeCarteBancaire.objects.get_or_create(
            name="China UnionPay", regex_pattern=r'^(62[0-9]{14,17})$')
        TypeCarteBancaire.objects.get_or_create(
            name="Diners Club Carte Blanche", regex_pattern=r'^30[0-5][0-9]{11}$')
        TypeCarteBancaire.objects.get_or_create(
            name="Diners Club International", regex_pattern=r'^36[0-9]{12}$')
