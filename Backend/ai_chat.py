from openai import OpenAI

# api key
API_KEY = "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"

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
