from django.conf import settings
import sqlite3
from django.http import JsonResponse
import requests
from openai import OpenAI
from django.apps import apps
from django.db.models import Field
from Accounts.models import *
from Hebergement.models import *
from TourOperateur.models import *
from Artisanal.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

api_key = settings.OPENAI_API_KEY


def get_model_structure():
    """
    Retourne la structure des modèles Django sous forme de dictionnaire.
    :return: dict
    """
    model_structure = {}

    for model in apps.get_models():
        model_name = model.__name__
        fields = model._meta.get_fields()
        field_list = []

        for field in fields:
            if isinstance(field, Field):
                field_list.append((field.name, field.get_internal_type()))

        model_structure[model_name] = field_list

    return model_structure


table_structure = get_model_structure()


def generate_django_query_with_gpt3(question, table_structure):
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Voici la structure simplifiée des modèles Django pour la base de données : {table_structure}\n\n"
        f"Question : {question}\n\n"
        f"Répondez avec l'expression Django QuerySet appropriée pour obtenir les résultats souhaités. "
        f"Ne fournissez aucune explication, juste le code du QuerySet. "
        f"Assurez-vous que la requête est valide et utilise correctement les champs et relations des modèles Django."
    )

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=250,
        temperature=0.7,
    )

    django_query = response.choices[0].text
    print(django_query)
    return django_query


def execute_and_display_query(django_query):
    try:
        if not isinstance(django_query, str):
            raise ValueError(
                "La requête générée n'est pas une chaîne de caractères valide."
            )

        query_result = eval(django_query)

        if hasattr(query_result, "values"):
            results = list(query_result.values())
        elif hasattr(query_result, "__dict__"):
            results = [query_result.__dict__]
        else:
            raise ValueError(
                "La requête générée ne renvoie pas un objet QuerySet ou un modèle valide."
            )

        results = [
            {k: v for k, v in result.items() if k != "_state"} for result in results
        ]

        return results

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return {"error": str(ve)}

    except Exception as e:
        print(f"Error executing Django query: {e}")
        return {"error": str(e)}


def get_user_request(message):
    try:
        sql_query = generate_django_query_with_gpt3(message, table_structure)
        result = execute_and_display_query(sql_query)
        if isinstance(result, dict) and "error" in result:
            return result
        return result
    except Exception as e:
        return {"error": str(e)}


def get_data_by_request(question):
    result = get_user_request(question)
    return result


@api_view(["POST"])
@permission_classes([AllowAny])
def test_database(request):
    question = "quel est la chambre le plus chère de votre site?"
    response = get_data_by_request(question)
    return Response({"response": response})


{"message": "quel est la chambre le plus chère de votre site?"}


def generate_sql_query_with_gpt3(question, table_structure):
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Voici la structure des tables de la base de données: {table_structure}\n"
        f"Question: {question}\n"
        f"Répondez avec la requête SQL appropriée pour obtenir les résultats souhaités."
    )

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=120,
        temperature=0.5,
    )

    sql_query = response.choices[0].text
    return sql_query
