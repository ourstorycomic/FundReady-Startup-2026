import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello, return JSON: {\"test\": 1}"}],
        model="openai/gpt-oss-120b",
        temperature=0.6,
        max_tokens=100,
        response_format={"type": "json_object"}
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", str(e))
