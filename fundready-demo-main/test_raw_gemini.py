import asyncio
import os
from api.gemini_client import get_client, prompt_template

async def test():
    content = open('../HoSo_Nexus_Digital_2026.txt', encoding='utf-8').read()
    prompt = prompt_template.format(document_type="pitchdeck", content=content, desired_amount="3 ty")
    from google.genai import types
    response = get_client().models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=8192,
            response_mime_type="application/json"
        )
    )
    with open("gemini_raw_output.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    asyncio.run(test())
