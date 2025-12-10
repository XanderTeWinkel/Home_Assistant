import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Key
API_KEY = os.getenv("API_KEY")

# Initialize client once
client = OpenAI(api_key=API_KEY)

def chat_with_ai(prompt: str) -> str:
    """
    Sends a prompt to the OpenAI API and returns the AI's response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content # type: ignore
