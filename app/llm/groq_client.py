import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm(system_prompt: str, user_prompt: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)