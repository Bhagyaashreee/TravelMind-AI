import asyncio

from agents import Runner

from backend.agents.destination_agent import destination_agent


async def main():
    result = await Runner.run(
        destination_agent,
        """
        I want to visit Goa for 4 days.

        My budget is ₹30,000.

        I like:
        - beaches
        - adventure
        - nightlife

        Suggest a practical travel plan.
        """
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())