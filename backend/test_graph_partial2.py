import asyncio

from backend.graph.destination_node import destination_node
from backend.graph.flight_node import flight_node
from backend.graph.hotel_node import hotel_node
from backend.graph.activity_node import activity_node


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
    result = await destination_node(state)
    state.update(result)

    print("✅ Destination result stored")

    print("\n✈️ Running Flight Node...")
    result = await flight_node(state)
    state.update(result)

    print("✅ Flight result stored")

    print("\n🏨 Running Hotel Node...")
    result = await hotel_node(state)
    state.update(result)

    print("✅ Hotel result stored")

    print("\n🎯 Running Activity Node...")
    result = await activity_node(state)
    state.update(result)

    print("✅ Activity result stored")

    print("\n" + "=" * 60)
    print("PARTIAL GRAPH TEST 2")
    print("=" * 60)

    print("\nState contains:")

    for key in state:
        print(f"- {key}")

    print("\n✅ Destination → Flight → Hotel → Activity works!")


if __name__ == "__main__":
    asyncio.run(main())