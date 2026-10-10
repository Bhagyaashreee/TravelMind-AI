from agents import Runner

from backend.agents.hotel_agent import hotel_agent
from backend.graph.state import TravelState
from backend.tools.hotel_tool import search_hotels


async def hotel_node(state: TravelState):

    print("\n🏨 Running Hotel Agent...")

    user_request = state["user_request"]

    # Temporary hotel search information.
    # Live hotel API will be connected later.
    hotel_data = search_hotels(
        destination="Goa, India",
        check_in="2026-10-15",
        check_out="2026-10-19",
        travelers=2
    )

    prompt = f"""
You are the Hotel Agent.

USER REQUEST:
{user_request}

HOTEL TOOL DATA:
{hotel_data}

Use ONLY the hotel tool data when discussing actual
hotel prices, ratings, availability, or amenities.

If the tool says that live data is unavailable:

- Do not invent hotel prices.
- Do not invent availability.
- Do not invent ratings.
- Do not invent reviews.
- Do not invent amenities.
- Clearly state that live hotel data is unavailable.
- Give only general accommodation advice.

Return a concise hotel planning result.
"""

    result = await Runner.run(
        hotel_agent,
        prompt
    )

    print("✅ Hotel Agent finished")

    return {
    "hotel_result": result.final_output,
    "live_hotel_data": False
}