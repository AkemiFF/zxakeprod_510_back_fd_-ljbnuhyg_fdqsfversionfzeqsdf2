import json
import time
import openai
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

from ChatBot.assistant import *
from ChatBot.utils import get_data_by_request


api_key = settings.OPENAI_API_KEY
# assistant = Assistant()


@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot(request):
    client = OpenAI(api_key=api_key)

    user_message = request.data.get("message")

    if not user_message:
        return Response(
            {"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150,
            temperature=0.7,
        )
        chatbot_response = response.choices[0].message.content
        return Response({"response": chatbot_response})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def chat_message_query(user_message, data_gets_by_user_query):
    client = OpenAI(api_key=api_key)

    try:
        thread = client.beta.threads.create()
        print(data_gets_by_user_query)
        contenue = f"""voici les données en temps réel obtenues nécéssaite au requete de l'utilisateur : {data_gets_by_user_query}"""

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="assistant",
            content=contenue,
        )

        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_QTdB1rb4O2zNTfr4bknHCKcV",
            model="gpt-3.5-turbo",
            temperature=0.7,
        )

        run_status = run.status
        while run_status in ["queued", "running"]:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            run_status = run.status

        if run_status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_response = None
            for msg in messages:
                if msg.role == "assistant":
                    assistant_response = msg.content[0].text.value
                    break

            if assistant_response:
                return {"response": assistant_response}
            else:
                return {"error": "No response from the assistant"}
        else:
            return {"error": "The run did not complete successfully"}

    except Exception as e:
        return {"error": str(e)}


@api_view(["POST"])
@permission_classes([AllowAny])
def test_chatbot_2(request):
    user_message = request.data.get("message")

    if not user_message:
        return Response(
            {"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    data_gets_by_user_query = get_data_by_request(user_message)
    result = chat_message_query(user_message, data_gets_by_user_query)

    if "error" in result:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(result)


@api_view(["POST"])
@permission_classes([AllowAny])
def test_chatbot(request):
    user_message = request.data.get("message")
    client = OpenAI(api_key=api_key)

    if not user_message:
        return Response(
            {"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="assistant"
        )

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_QTdB1rb4O2zNTfr4bknHCKcV",
            model="gpt-3.5-turbo",
            temperature=0.7,
        )

        run_status = run.status
        while run_status in ["queued", "running"]:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            run_status = run.status

        if run_status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_response = None
            for msg in messages:
                if msg.role == "assistant":
                    assistant_response = msg.content[0].text.value
                    break

            if assistant_response:
                return Response({"response": assistant_response})
            else:
                return Response(
                    {"error": "No response from the assistant"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "The run did not complete successfully"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
