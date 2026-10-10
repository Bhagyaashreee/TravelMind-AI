import asyncio

from agents import Runner

from backend.agents.safety_agent import safety_agent
from backend.tools.weather_tool import get_weather


async def main():

    weather = get_weather("Goa, India")

    print("\n🌦️ WEATHER DATA")
    print(weather)

    prompt = f"""
You are the Safety Agent for a travel planning system.

Destination: Goa, India

REAL WEATHER DATA:
{weather}

Based on this weather data, give practical travel safety advice.

Include:
1. Weather conditions
2. Outdoor activity precautions
3. Beach/water safety
4. General travel safety

Do not invent weather information.
Clearly use the provided weather data.
"""

    print("\n🛡️ Running Safety Agent...")

    result = await Runner.run(
        safety_agent,
        prompt,
    )

    print("\n✅ SAFETY RESULT")
    print("=" * 60)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())