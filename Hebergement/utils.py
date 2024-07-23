from openai import OpenAI


def generer_description_hebergement(api_key, hebergement_info):
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Nom de l'hébergement : {hebergement_info['nom_hebergement']}\n"
        f"Localisation : {hebergement_info['localisation']}\n"
        f"Description : {hebergement_info['description_hebergement']}\n"
        f"Nombre d'étoiles : {hebergement_info['nombre_etoile_hebergement']}\n"
        f"Type d'hébergement : {hebergement_info['type_hebergement']}\n"
        f"Accessoires : {', '.join(hebergement_info['accessoires'])}\n"
        "Générez une description attrayante pour cet hébergement en mettant en avant ses atouts et sa localisation."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=180,
        temperature=0.7,
    )

    description = response.choices[0].message.content
    return description
