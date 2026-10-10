import asyncio

from agents import Runner

from backend.agents.safety_agent import safety_agent


async def main():

    result = await Runner.run(
        safety_agent,
        """
        I am planning a 4-day trip to Goa.

        Travelers: 2
        Budget: ₹30,000

        We are interested in:
        - Beaches
        - Water sports
        - Adventure activities
        - Nightlife

        What safety precautions should we consider?
        """,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())