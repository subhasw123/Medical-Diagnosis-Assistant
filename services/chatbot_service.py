from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("API_KEY")
)

def ask_chatbot(question):

    prompt = f"""
You are a medical assistant.

Answer in simple language.

Question:
{question}

Add a disclaimer that this is not professional medical advice.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text