from dotenv import load_dotenv
import os
from google import genai
from database.db import get_connection

load_dotenv()

client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def log_chatbot_interaction(question, answer, ip_address=None, user_agent=None):
    """Persist chatbot Q&A to the chatbot_logs table."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chatbot_logs (question, answer, ip_address, user_agent) VALUES (%s, %s, %s, %s)",
            (question, answer, ip_address, user_agent)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        # Non-critical — log silently so chatbot still works if DB is down
        print(f"[chatbot_log] Warning: could not save log: {e}")


def ask_chatbot(question, ip_address=None, user_agent=None):

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

    answer = response.text

    # Log to DB asynchronously
    log_chatbot_interaction(question, answer, ip_address, user_agent)

    return answer