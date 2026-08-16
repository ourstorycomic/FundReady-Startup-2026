import asyncio
from api.gemini_client import analyze_with_gemini
import traceback

async def test():
    try:
        content = open('../HoSo_Nexus_Digital_2026.txt', encoding='utf-8').read()
        res = await analyze_with_gemini('pitchdeck', content, '3 ty')
        print("Success:", res)
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
