import asyncio

from backend.graph.budget_node import budget_node


async def main():

    state = {
        "user_request": """
        I want to travel from Hyderabad to Goa.

        Trip duration: 4 days
        Travelers: 2
        Total budget: ₹30,000

        My interests are:
        - beaches
        - adventure
        - nature
        - nightlife
        """
    }

    print("\n💰 Running Budget Node...")

    result = await budget_node(state)

    print("\n" + "=" * 60)
    print("BUDGET NODE RESULT")
    print("=" * 60)

    print("\nAI BUDGET ANALYSIS:")
    print(result["budget_result"])

    print("\n" + "-" * 60)
    print("BUDGET STATUS")
    print("-" * 60)

    print("Total Budget:", result["total_budget"])
    print("Status:", result["budget_status"])

    if result["budget_status"] == "price_data_unavailable":

        print("\n⚠️ Live price data is unavailable.")
        print("The trip cost cannot currently be calculated.")

    else:

        print("\n" + "-" * 60)
        print("PYTHON BUDGET CALCULATION")
        print("-" * 60)

        print("Flight Cost:", result["flight_cost"])
        print("Hotel Cost:", result["hotel_cost"])
        print("Food Cost:", result["food_cost"])
        print("Transportation Cost:", result["transportation_cost"])
        print("Activity Cost:", result["activity_cost"])
        print("Emergency Cost:", result["emergency_cost"])

        print("Estimated Total:", result["estimated_total"])
        print("Remaining/Excess:", result["remaining_budget"])


if __name__ == "__main__":
    asyncio.run(main())