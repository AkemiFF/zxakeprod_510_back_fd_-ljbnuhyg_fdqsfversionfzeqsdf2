from openai import OpenAI
from django.conf import settings

from Hebergement.models import Hebergement

api_key = settings.OPENAI_API_KEY


def get_hebergement_data():
    hebergements = Hebergement.objects.all()
    data = ""
    for hebergement in hebergements:
        data += f"Nom: {hebergement.nom_hebergement}\nDescription: {hebergement.description_hebergement}\n"

    return data


def Assistant():
    client = OpenAI(api_key=api_key)
    assistant = client.beta.assistants.create(
        name="Travel Advisor",
        instructions=(
            "You are a travel advisor assistant who work for Aftrip, a website concerning travel advisor. "
            "Your job is to answer questions and provide advice about accommodations, "
            "tour operators, and artisanal products available on the website. "
            "If the question is not related to these topics, kindly inform the user that you can only assist with these specific areas."
        ),
        model="gpt-3.5-turbo",
    )
    return assistant


#
