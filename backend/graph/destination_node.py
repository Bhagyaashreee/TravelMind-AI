from agents import Runner

from backend.agents.destination_agent import destination_agent
from backend.graph.state import TravelState


async def destination_node(state: TravelState):

    result = await Runner.run(
        destination_agent,
        state["user_request"],
    )

    return {
        "destination_result": result.final_output
    }