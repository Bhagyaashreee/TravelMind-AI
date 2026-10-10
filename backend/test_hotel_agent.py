import asyncio

from agents import Runner

from backend.agents.hotel_agent import hotel_agent


async def main():

    result = await Runner.run(
        hotel_agent,
        """
        I want to visit Goa for 4 days.

        Travelers: 2
        Budget: ₹30,000

        I like:
        - beaches
        - adventure
        - nightlife

        Suggest suitable areas and types of hotels
        I should look for.
        """
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())