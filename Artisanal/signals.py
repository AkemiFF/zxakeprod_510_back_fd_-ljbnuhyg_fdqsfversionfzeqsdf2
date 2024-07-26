from django.db.models.signals import post_migrate
from django.dispatch import receiver
import Accounts
from Accounts.models import TypeCarteBancaire, TypeResponsable
from Artisanal.models import Specification


INITIAL_SPECIFICATIONS = [
    "Handmade",
    "Organic",
    "Eco-friendly",
    "Limited Edition",
    "Customizable",
    "Fair Trade",
    "Locally Sourced",
    "Recycled Materials",
    "Biodegradable",
    "Vegan",
    "Cruelty-Free",
    "Artisanal",
    "Zero Waste",
    "Sustainable",
    "BPA-Free",
    "Non-Toxic",
    "Carbon Neutral",
    "Renewable Resources",
    "Plastic-Free",
    "Energy Efficient",
    "Upcycled",
    "Ethically Made",
    "Waterproof",
    "Heat Resistant",
    "Hypoallergenic",
    "Anti-Bacterial",
    "Eco-Friendly Packaging",
    "Hand-Painted",
    "Natural Ingredients",
    "Organic Cotton",
    "Solar Powered",
    "Compostable",
    "Durable",
    "Lightweight",
    "Versatile",
    "Handcrafted",
    "Locally Made",
    "Limited Production",
    "Exclusive Design",
]


@receiver(post_migrate)
def create_initial_types(sender, **kwargs):
    for spec in INITIAL_SPECIFICATIONS:
        Specification.objects.get_or_create(type_specification=spec)
