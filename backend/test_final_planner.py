import asyncio

from agents import Runner

from backend.agents.final_planner_agent import final_planner_agent


async def main():

    result = await Runner.run(
        final_planner_agent,
        """
        Create a sample final travel plan.

        Destination: Goa
        Duration: 4 days
        Travelers: 2
        Budget: ₹30,000

        Interests:
        - Beaches
        - Adventure
        - Nature
        - Nightlife

        Destination Agent:
        Goa is suitable for beaches, adventure and nightlife.
        Recommended areas include Calangute and Baga.

        Flight Agent:
        Look for economical flights between Hyderabad and Goa.
        Exact prices and availability must be verified.

        Hotel Agent:
        Consider budget-friendly accommodation around
        Calangute, Candolim or similar areas.
        Exact prices must be verified.

        Activity Agent:
        Suggested activities include beaches,
        water activities, nature experiences and nightlife.
        Exact prices and availability must be verified.

        Safety Agent:
        Take precautions with belongings, road travel,
        water activities and crowded areas.

        Budget Agent:
        Estimated trip cost may exceed ₹30,000.
        Reduce accommodation, food or activities if necessary.

        Combine this information into one practical
        4-day travel itinerary.
        """,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())