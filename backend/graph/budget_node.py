
import re

from agents import Runner

from backend.agents.budget_agent import budget_agent
from backend.graph.state import TravelState


def extract_budget(user_request: str) -> int:
    """Extract the user's total trip budget from their request."""

    text = user_request.lower().replace(",", "")

    patterns = [
        r"(?:under|below|within|less than)\s*(?:₹|rs\.?|inr)?\s*(\d+)",
        r"(?:total budget|budget)\s*(?:is|of|:|-)?\s*(?:₹|rs\.?|inr)?\s*(\d+)",
        r"(?:₹|rs\.?|inr)\s*(\d+)",
        r"(\d+)\s*budget",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return 0


async def budget_node(state: TravelState):
    print("\n💰 Running Budget Agent...")

    user_request = state["user_request"]
    total_budget = extract_budget(user_request)

    print(f"💰 Detected user budget: ₹{total_budget:,}")

    flight_cost = state.get("flight_cost")
    demo_flight_data = state.get("demo_flight_data", False)
    live_flight_data = state.get("live_flight_data", False)

    # Never count demo flight prices as verified costs.
    if demo_flight_data:
        usable_flight_cost = None
    else:
        usable_flight_cost = flight_cost

    prompt = f"""
Analyze this travel request:

{user_request}

Total user budget: ₹{total_budget:,}

Flight cost supplied by the system: {flight_cost}
Is flight data demo data? {demo_flight_data}
Is flight data live data? {live_flight_data}

Rules:
- Never describe demo prices as live or verified prices.
- Do not invent hotel, food, transport, activity, or emergency costs.
- Do not claim the trip fits the budget without sufficient cost data.
- Clearly distinguish known prices from estimates and unavailable prices.
- The user's budget is the total budget for the trip.
"""

    result = await Runner.run(budget_agent, prompt)
    budget_analysis = result.final_output

    # Demo data is excluded from all real budget calculations.
    if demo_flight_data:
        final_result = f"""
## Budget Analysis

{budget_analysis}

## Price Verification

The available flight information is demo/test data, not a
verified live fare. It has not been counted as an actual trip cost.

Total user budget: ₹{total_budget:,}

Hotel, food, transportation, activities, and emergency costs
have not been verified.

## Budget Status

The complete trip cost cannot currently be verified.
No remaining budget or budget surplus has been calculated.
"""

        status = "demo_data_excluded"

    elif usable_flight_cost is not None and live_flight_data:
        final_result = f"""
## Budget Analysis

{budget_analysis}

## Available Cost

Verified live flight cost supplied by the system: ₹{usable_flight_cost:,.0f}

Other trip costs have not been verified.

Total user budget: ₹{total_budget:,}

## Budget Status

The complete trip cost cannot yet be verified.
The flight cost alone is not enough to determine whether
the entire trip fits within the budget.
"""

        status = "partial_live_data"

    else:
        final_result = f"""
## Budget Analysis

{budget_analysis}

Total user budget: ₹{total_budget:,}

No verified flight cost is currently available.
Hotel, food, transportation, activity, and emergency costs
also remain unverified.

The complete trip cost cannot currently be verified.
No remaining budget or budget surplus has been calculated.
"""

        status = "price_data_unavailable"

    print(f"📊 Budget status: {status}")
    print("✅ Budget Agent finished")

    return {
        "budget_result": final_result,
        "total_budget": total_budget,
        "budget_status": status,
    }
