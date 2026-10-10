import asyncio

from backend.graph.travel_graph import travel_graph


async def main():

    initial_state = {
        "user_request": """
        I want to travel from Hyderabad to Goa.

        Trip duration: 4 days
        Travelers: 2
        Budget: ₹30,000

        My interests are:
        - beaches
        - adventure
        - nature
        - nightlife
        """,
    }

    result = await travel_graph.ainvoke(initial_state)

    print("\n")
    print("=" * 70)
    print("FINAL TRAVEL PLAN")
    print("=" * 70)
    print(result["final_plan"])


if __name__ == "__main__":
    asyncio.run(main())