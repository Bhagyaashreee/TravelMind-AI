import os, asyncio
from dotenv import load_dotenv
load_dotenv('.env')
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
        api_key=os.environ.get('GEMINI_API_KEY'),
        timeout=10
    )
    res = await client.chat.completions.create(
        model='gemini-3.5-flash-lite',
        messages=[{'role': 'user', 'content': 'hi'}]
    )
    print(res.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())
