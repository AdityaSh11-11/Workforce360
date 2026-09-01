import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://openrouter.ai/api/v1/chat/completions"

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "deepseek/deepseek-chat-v3-0324:free"
)


def ask_workforce_ai(df, question):

    context = df.head(200).to_csv(index=False)

    prompt = f"""
    You are HR AI Assistant.

    Workforce Dataset Sample:

    {context}

    Answer user's question only from dataset.

    Question:
    {question}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(URL, headers=headers, json=body, timeout=60)

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]