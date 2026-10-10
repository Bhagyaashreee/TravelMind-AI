
from agents import Runner

from backend.agents.activity_agent import activity_agent
from backend.graph.state import TravelState
from backend.tools.activity_tool import search_activities


async def activity_node(state: TravelState):
    print("\n🎯 Running Activity Agent...")

    user_request = state["user_request"]

    # No live activity API is connected yet.
    activity_data = search_activities(
        destination="",
        interests=[],
    )

    print("\n🎯 Activity Tool Result:")
    print(activity_data)

    prompt = f"""
You are the Activity Agent in TravelMind AI.

USER REQUEST:
{user_request}

ACTIVITY TOOL DATA:
{activity_data}

RULES:
- No live activity API is connected.
- Do not invent activity prices, discounts, schedules,
  opening hours, offers, or availability.
- You may recommend general activities based on the user's
  destination and interests.
- Clearly label these as general recommendations, not verified
  live listings.
- Do not create a separate activity budget.

For each suggested activity, provide:
1. Activity or experience
2. Category
3. Why it may suit the traveler
4. Suggested duration, clearly marked as an estimate
5. Booking and verification note

State that live activity prices and availability are unavailable.
Return a concise activity planning result.
"""

    result = await Runner.run(activity_agent, prompt)

    print("✅ Activity Agent finished")

    return {
        "activity_result": result.final_output,
        "live_activity_data": False,
    }
