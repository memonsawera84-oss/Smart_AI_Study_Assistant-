import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Exact .env location
ENV_FILE = BASE_DIR / ".env"

# Load .env
load_dotenv(dotenv_path=ENV_FILE)

api_key = os.getenv("GROQ_API_KEY")

print("ENV FILE:", ENV_FILE)
print("GROQ API KEY FOUND:", bool(api_key))
client = Groq(api_key=api_key) if api_key else None


def ask_ai(prompt, language="English"):

    if client is None:
        return "Error: GROQ_API_KEY is not configured. Check your .env file."

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
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"