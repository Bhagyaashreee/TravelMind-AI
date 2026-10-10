import asyncio

from backend.graph.destination_node import destination_node
from backend.graph.flight_node import flight_node


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

    print("\n🗺️ Running Destination Node...")

    destination_result = await destination_node(state)

    state.update(destination_result)

    print("✅ Destination result stored in state")

    print("\n✈️ Running Flight Node...")

    flight_result = await flight_node(state)

    state.update(flight_result)

    print("✅ Flight result stored in state")

    print("\n" + "=" * 60)
    print("PARTIAL GRAPH TEST")
    print("=" * 60)

    print("\nState contains:")

    for key in state:
        print(f"- {key}")

    print("\n✅ Destination → Flight connection works!")


if __name__ == "__main__":
    asyncio.run(main())