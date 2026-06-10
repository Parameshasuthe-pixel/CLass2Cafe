from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


def ask_ai(message):

    key = os.environ.get("GROQ_API_KEY")

    client = Groq(
        api_key=key
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are an intent classifier.

Return ONLY ONE WORD from this list:

coffee
sandwich
samosa
menu
crowd
track
cancel
feedback
recommend
greeting
unknown

Do not explain anything.
Do not write sentences.
Only return one word.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()