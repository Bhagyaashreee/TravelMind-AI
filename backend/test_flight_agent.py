import asyncio

from agents import Runner

from backend.agents.flight_agent import flight_agent


async def main():

    result = await Runner.run(
        flight_agent,
        """
        I want to travel from Hyderabad to Goa.

        Trip duration: 4 days
        Travelers: 2
        Budget: ₹30,000

        Tell me what kind of flight options I should look for.
        """
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())