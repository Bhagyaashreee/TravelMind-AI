import asyncio

from backend.graph.safety_node import safety_node


async def main():

    state = {
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
        """
    }

    result = await safety_node(state)

    print("\n" + "=" * 60)
    print("DYNAMIC SAFETY RESULT")
    print("=" * 60)
    print(result["safety_result"])


if __name__ == "__main__":
    asyncio.run(main())