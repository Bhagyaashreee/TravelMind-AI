import re

from agents import Runner

from backend.agents.budget_agent import budget_agent
from backend.graph.state import TravelState
from backend.tools.budget_tool import estimate_trip_budget


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


def extract_travelers(user_request: str) -> tuple[int, bool]:
    """Extract the number of travelers from request, returning (count, is_explicit)."""
    text = user_request.lower()

    if re.search(r"\b(?:solo|alone)\b", text):
        return 1, True
    if re.search(r"\b(?:couple|pair|2 of us|two of us)\b", text):
        return 2, True

    match = re.search(r"(\d+)\s*(?:travelers?|travellers?|people|persons?|adults?|guests?)", text)
    if match:
        return max(1, int(match.group(1))), True

    match = re.search(r"(?:for)\s*(\d+)\s*(?:travelers?|travellers?|people|persons?|adults?)?", text)
    if match:
        return max(1, int(match.group(1))), True

    # Default assumed: 2 travelers
    return 2, False


def extract_duration(user_request: str) -> tuple[int, bool]:
    """Extract trip duration in days from request, returning (days, is_explicit)."""
    text = user_request.lower()

    match = re.search(r"(\d+)\s*(?:days?|day)\b", text)
    if match:
        return max(1, int(match.group(1))), True

    match = re.search(r"(\d+)\s*(?:nights?|night)\b", text)
    if match:
        return max(1, int(match.group(1)) + 1), True

    if "weekend" in text:
        return 2, True

    # Default assumed: 3 days
    return 3, False


async def budget_node(state: TravelState):
    print("\n💰 Running Budget Agent...")

    user_request = state["user_request"]
    total_budget = extract_budget(user_request)
    travelers, travelers_explicit = extract_travelers(user_request)
    duration_days, duration_explicit = extract_duration(user_request)

    flight_cost = state.get("flight_cost")
    live_flight_data = state.get("live_flight_data", False)

    # Calculate budget breakdown using deterministic tool logic
    budget_data = estimate_trip_budget(
        total_budget=total_budget,
        travelers=travelers,
        duration_days=duration_days,
        live_flight_cost=flight_cost if live_flight_data else None,
    )

    breakdown = budget_data["breakdown"]
    assumptions = budget_data["assumptions"]
    estimated_total = budget_data["estimated_total"]
    remaining_budget = budget_data["remaining_budget"]
    status = budget_data["status"]
    excess_or_deficit = budget_data["remaining_or_excess"]

    # Construct assumptions text
    assumption_notes = []
    if not travelers_explicit:
        assumption_notes.append("Number of travelers assumed: 2 (not specified in request)")
    else:
        assumption_notes.append(f"Number of travelers: {travelers}")

    if not duration_explicit:
        assumption_notes.append("Trip duration assumed: 3 days / 2 nights (not specified in request)")
    else:
        assumption_notes.append(f"Trip duration: {duration_days} days / {assumptions['nights']} nights")

    if total_budget == 0:
        assumption_notes.append("Target budget: Not specified (provided baseline estimated cost)")
    else:
        assumption_notes.append(f"User target budget: ₹{total_budget:,}")

    assumption_notes.append(f"Accommodation: {assumptions['room_sharing']}")
    assumption_notes.append(f"Transportation: {assumptions['transportation_type']}")
    assumption_notes.append("Pricing status: All values are planning estimates (not live booking quotes)")

    assumptions_str = "\n".join(f"- {note}" for note in assumption_notes)

    prompt = f"""
Analyze this travel request and present the calculated budget breakdown:

USER REQUEST:
{user_request}

TRIP PARAMETERS & STATED ASSUMPTIONS:
{assumptions_str}

PRE-CALCULATED BUDGET DATA (Calculated by Budget Tool):
- Target Budget: ₹{total_budget:,.2f}
- Transportation (Intercity): ₹{breakdown['transportation']:,.2f} [{'Verified Live Data' if assumptions['is_live_transport'] else 'Estimated'}]
- Accommodation: ₹{breakdown['accommodation']:,.2f} [Estimated]
- Food & Dining: ₹{breakdown['food']:,.2f} [Estimated]
- Local Transport: ₹{breakdown['local_transport']:,.2f} [Estimated]
- Activities & Sightseeing: ₹{breakdown['activities']:,.2f} [Estimated]
- Emergency Contingency Buffer: ₹{breakdown['emergency']:,.2f} [Estimated]
--------------------------------------------------
- Total Estimated Trip Cost: ₹{estimated_total:,.2f}
- Difference vs Target Budget: {'₹' + f'{remaining_budget:,.2f} surplus' if status == 'within_budget' else '₹' + f'{excess_or_deficit:,.2f} deficit' if status == 'over_budget' else 'Exact match'}
- Budget Status: {status} (Fits Budget: {'YES' if budget_data['fits_budget'] else 'NO' if budget_data['fits_budget'] is False else 'N/A'})

INSTRUCTIONS:
- Present the full estimated breakdown clearly with all 6 categories.
- Clearly label each category as [Estimated] or [Verified Live Data].
- Explicitly compare Total Estimated Cost against User Budget and clearly state whether it fits.
- List the stated assumptions clearly.
- Include 2-3 practical money-saving suggestions.
- Remind the user that estimates are for planning purposes and live prices should be checked before booking.
"""

    result = await Runner.run(budget_agent, prompt)
    budget_analysis = result.final_output

    print(f"💰 Total Budget: ₹{total_budget:,}")
    print(f"📊 Estimated Total: ₹{estimated_total:,.2f} | Status: {status}")
    print("✅ Budget Agent finished")

    return {
        "budget_result": budget_analysis,
        "total_budget": float(total_budget),
        "flight_cost": float(breakdown["transportation"]),
        "hotel_cost": float(breakdown["accommodation"]),
        "food_cost": float(breakdown["food"]),
        "transportation_cost": float(breakdown["local_transport"]),
        "local_transport_cost": float(breakdown["local_transport"]),
        "activity_cost": float(breakdown["activities"]),
        "emergency_cost": float(breakdown["emergency"]),
        "estimated_total": float(estimated_total),
        "remaining_budget": float(remaining_budget),
        "budget_status": status,
    }
