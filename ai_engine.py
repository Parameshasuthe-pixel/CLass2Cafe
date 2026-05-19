from groq import Groq

client = Groq(
    api_key="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"
)

def ask_ai(message):

    response = client.chat.completions.create(
        model="llama3-70b-8192",
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