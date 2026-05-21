import os

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def summarize_text(text):

    prompt = f"Summarize this text:\n{text}"

    response = client.chat.completions.create(
          model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content