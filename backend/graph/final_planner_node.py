from agents import Runner
from backend.agents.final_planner_agent import final_planner_agent
from backend.graph.state import TravelState

async def final_planner_node(state: TravelState):
    print("\n📝 Running Final Planner Agent...")

    prompt = f"""
You are the Final Travel Planner. Combine the information provided by the other agents into a single, cohesive travel plan.

DESTINATION:
{state.get('destination_result', 'Not available')}

FLIGHT:
{state.get('flight_result', 'Not available')}

HOTEL:
{state.get('hotel_result', 'Not available')}

ACTIVITY:
{state.get('activity_result', 'Not available')}

SAFETY:
{state.get('safety_result', 'Not available')}

BUDGET:
{state.get('budget_result', 'Not available')}

RULES:
- Present the information clearly.
- Include the complete Estimated Budget Breakdown (transportation, accommodation, food, local transport, activities, emergency contingency) and budget comparison from the BUDGET section.
- Present the budget breakdown in a standard Markdown table with headers: | Category | Estimated Cost | Details / Status |, surrounded by blank lines. Do not place heading tags or extra linebreaks inside table cells.
- Preserve all [Estimated] labels and disclaimers.
- Do not invent separate prices or create a conflicting total cost. Rely entirely on the BUDGET section provided above.
- If an agent stated that live data is unavailable, preserve that statement.
"""

    result = await Runner.run(final_planner_agent, prompt)
    print("✅ Final Planner Agent finished")

    return {
        "final_plan": result.final_output
    }
