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


api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=api_key)
assistant = Assistant()


@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot(request):
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


@api_view(["POST"])
@permission_classes([AllowAny])
def test_chatbot(request):
    user_message = request.data.get("message")

    if not user_message:
        return Response(
            {"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        thread = client.beta.threads.create()
        hebergement_data = get_hebergement_data()
        # client.beta.threads.messages.create(
        #     thread_id=thread.id,
        #     role="assistant",
        #     content=f"Here is the information about all the accommodations:\n{hebergement_data}",
        # )

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
