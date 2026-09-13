import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


def ask_ai(prompt, language="English"):

    if client is None:
        return (
            "Error: GROQ_API_KEY is not configured. "
            "Add it to Streamlit Secrets or the .env file."
        )

    system_prompt = f"""
You are Smart AI Study Assistant.

Answer in {language}.

Explain everything simply for students.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=2048
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {e}"