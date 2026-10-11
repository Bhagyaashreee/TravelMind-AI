from agents import Runner

from backend.agents.flight_agent import flight_agent
from backend.graph.state import TravelState
from backend.tools.flight_tool import search_flights


async def flight_node(state: TravelState):
    print("\n✈️ Running Flight Agent...")

    user_request = state["user_request"]

    # Call the tool. Currently this returns unavailable.
    flight_data = search_flights(
        origin="HYD",
        destination="GOI",
        departure_date="2026-10-15",
    )

    print("\n✈️ Flight Tool Result:")
    print(flight_data)

    is_live_data = flight_data.get("status") == "live_data"

    prompt = f"""
You are the Flight Agent in TravelMind AI.

USER REQUEST:
{user_request}

FLIGHT DATA:
{flight_data}

DATA STATUS:
Live data: {is_live_data}

RULES:
- Use only the flight information supplied by the tool.
- Never invent flights, airlines, prices, schedules, or availability.
- If no flight data is available, explicitly state that prices and availability cannot currently be verified.
- Do not claim a flight is available for booking unless the source explicitly confirms availability.
- Compare supplied flights by price, duration, and stops only when those values are present.

Return a concise flight planning result.
"""

    result = await Runner.run(flight_agent, prompt)

    print("✅ Flight Agent finished")

    flight_cost = None

    flights = flight_data.get("flights", [])

    if is_live_data and flights:
        prices = []

        for flight in flights:
            price = flight.get("price")

            try:
                parsed_price = float(price)

                if parsed_price >= 0:
                    prices.append(parsed_price)
            except (TypeError, ValueError):
                continue

        if prices:
            flight_cost = min(prices)

    print(f"✈️ Verified live flight cost: {flight_cost}")

    return {
        "flight_result": result.final_output,
        "live_flight_data": is_live_data,
        "demo_flight_data": False,
        "flight_cost": flight_cost,
    }
