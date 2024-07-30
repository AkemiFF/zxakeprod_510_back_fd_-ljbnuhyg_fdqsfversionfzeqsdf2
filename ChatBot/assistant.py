from openai import OpenAI
from django.conf import settings

from ChatBot.helpers import get_model_structure
from Hebergement.models import Hebergement

api_key = settings.OPENAI_API_KEY


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


def DatabaseAssistant():
    table_structure = get_model_structure()

    client = OpenAI(api_key=api_key)
    instruction = f"""
    You are a database assistant. Here is the simplified structure of the Django models for the database: {table_structure}
    
    Respond with the appropriate Django QuerySet expression to obtain the desired results. Do not provide any explanation, just the QuerySet code.
    
    Ensure that the query is valid and correctly uses the fields and relationships from the Django models.
    """

    assistant = client.beta.assistants.create(
        name="Database Manager Assistant",
        instructions=instruction,
        model="gpt-3.5-turbo",
    )
    return assistant
