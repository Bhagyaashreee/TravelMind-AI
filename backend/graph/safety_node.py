from agents import Runner

from backend.agents.safety_agent import safety_agent
from backend.graph.state import TravelState
from backend.tools.weather_tool import get_weather


def extract_destination(user_request: str):
    """
    Extract the destination from a travel request.
    """

    text = user_request.lower()

    if "to goa" in text:
        return "Goa, India"

    if "to manali" in text:
        return "Manali, India"

    if "to mumbai" in text:
        return "Mumbai, India"

    if "to delhi" in text:
        return "Delhi, India"

    if "to hyderabad" in text:
        return "Hyderabad, India"

    return None


async def safety_node(state: TravelState):

    print("\n🛡️ Running Safety Agent...")

    user_request = state["user_request"]

    # ---------------------------------------------------------
    # EXTRACT DESTINATION
    # ---------------------------------------------------------

    destination = extract_destination(user_request)

    # ---------------------------------------------------------
    # GET WEATHER DATA SAFELY
    # ---------------------------------------------------------

    if destination:

        try:
            weather = get_weather(destination)

        except Exception as e:

            print(f"⚠️ Weather data unavailable: {e}")

            weather = {
                "error": "Weather API is currently unavailable."
            }

    else:

        weather = {
            "error": "Destination could not be identified."
        }

    # ---------------------------------------------------------
    # SAFETY AGENT PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are the Safety Agent in a travel planning system.

USER REQUEST:
{user_request}

DESTINATION:
{destination}

REAL WEATHER DATA:
{weather}

Your task is ONLY to provide safety advice based on the
provided weather information and general travel precautions.

==================================================
WEATHER INTERPRETATION
==================================================

temperature_2m = current temperature in Celsius.

relative_humidity_2m = current humidity percentage.

wind_speed_10m = current wind speed in km/h.

precipitation = current precipitation in mm.

temperature_2m_max = daily maximum temperature.

temperature_2m_min = daily minimum temperature.

precipitation_probability_max = maximum probability of
precipitation for that day, expressed as a percentage.

weather_code represents the weather condition.


==================================================
CURRENT WEATHER DATA
==================================================

Current precipitation:

{weather.get("current", {}).get(
    "precipitation",
    "unavailable"
)}

Forecast precipitation probabilities:

{weather.get("daily", {}).get(
    "precipitation_probability_max",
    "unavailable"
)}


==================================================
IMPORTANT WEATHER AVAILABILITY RULE
==================================================

If the weather data contains:

"Weather API is currently unavailable."

then clearly state:

"Live weather data is currently unavailable."

Do NOT invent:

- temperature
- rainfall
- humidity
- wind speed
- weather conditions
- weather alerts
- forecasts


==================================================
SAFETY INFORMATION
==================================================

Provide:

1. Current weather conditions
2. Four-day weather summary
3. Temperature precautions
4. Rain precautions
5. Wind precautions
6. Outdoor activity precautions
7. Beach/water safety if relevant
8. General travel preparation


==================================================
STRICT RULES
==================================================

- Use actual numbers from the weather data when available.
- Do NOT invent weather information.
- Do NOT invent current alerts or warnings.
- Do NOT claim floods, droughts, crime problems, diseases,
  dangerous roads, protests, or other current risks unless
  explicitly provided in the input.
- Do NOT provide budget recommendations.
- Do NOT discuss flights or hotels.
- Do NOT make medical claims.
- If information is unavailable, explicitly say so.
- Keep the response concise and practical.
- Focus ONLY on travel safety.


==================================================
FINAL REQUIREMENT
==================================================

Never invent missing weather information.

If the weather API is unavailable, provide general
travel safety advice and clearly state that live weather
data is unavailable.
"""

    # ---------------------------------------------------------
    # RUN SAFETY AGENT
    # ---------------------------------------------------------

    result = await Runner.run(
        safety_agent,
        prompt,
    )

    print("✅ Safety Agent finished")

    return {
        "safety_result": result.final_output
    }