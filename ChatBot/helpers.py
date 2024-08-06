from django.apps import apps
from django.db.models import Field


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
