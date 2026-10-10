import asyncio

from backend.graph.destination_node import destination_node
from backend.graph.flight_node import flight_node
from backend.graph.hotel_node import hotel_node
from backend.graph.activity_node import activity_node
from backend.graph.safety_node import safety_node
from backend.graph.budget_node import budget_node
from backend.graph.final_planner_node import final_planner_node


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
    state.update(await destination_node(state))

    print("✈️ Running Flight Node...")
    state.update(await flight_node(state))

    print("🏨 Running Hotel Node...")
    state.update(await hotel_node(state))

    print("🎯 Running Activity Node...")
    state.update(await activity_node(state))

    print("🛡️ Running Safety Node...")
    state.update(await safety_node(state))

    print("💰 Running Budget Node...")
    state.update(await budget_node(state))

    print("\n🧠 Running Final Planner...")
    state.update(await final_planner_node(state))

    print("\n" + "=" * 70)
    print("FINAL TRAVEL PLAN")
    print("=" * 70)

    print(state["final_plan"])

    print("\n" + "=" * 70)
    print("FINAL STATE KEYS")
    print("=" * 70)

    for key in state:
        print(f"- {key}")


if __name__ == "__main__":
    asyncio.run(main())