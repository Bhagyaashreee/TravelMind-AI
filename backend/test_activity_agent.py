import asyncio

from agents import Runner

from backend.agents.activity_agent import activity_agent


async def main():

    result = await Runner.run(
        activity_agent,
        """
        I want to visit Goa for 4 days.

        Travelers: 2
        Budget: ₹30,000

        I like:
        - beaches
        - adventure
        - nightlife
        - nature

        Suggest activities that match my interests.
        """,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())