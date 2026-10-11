import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import openai

from backend.main import app, QUOTA_ERROR_MESSAGE
from backend.graph.travel_graph import travel_graph
from backend.agents.destination_agent import destination_agent
from backend.agents.flight_agent import flight_agent
from backend.agents.hotel_agent import hotel_agent
from backend.agents.activity_agent import activity_agent
from backend.agents.safety_agent import safety_agent
from backend.agents.budget_agent import budget_agent
from backend.agents.final_planner_agent import final_planner_agent


@pytest.fixture
def client():
    return TestClient(app)


class MockAgentRunResult:
    def __init__(self, output_text: str):
        self.final_output = output_text


def test_all_seven_agents_called_exactly_once_per_trip_request():
    """Verify that one complete trip request executes all 7 agents exactly once (7 API calls total)."""
    async def _run():
        call_records = []

        async def mock_runner_run(agent, prompt, *args, **kwargs):
            agent_name = getattr(agent, "name", str(agent))
            call_records.append(agent_name)
            return MockAgentRunResult(f"Mocked output for {agent_name}")

        with patch("agents.Runner.run", side_effect=mock_runner_run), \
             patch("backend.graph.safety_node.get_weather", return_value={"current": {}, "daily": {}}):
            
            initial_state = {
                "user_request": "Plan a 4 day trip from Hyderabad to Goa for 2 travelers under ₹30,000."
            }

            result = await travel_graph.ainvoke(initial_state)

            # 1. Total Gemini API calls must be exactly 7
            assert len(call_records) == 7, f"Expected 7 agent calls, got {len(call_records)}: {call_records}"

            # 2. Verify all seven distinct agents were called in order
            expected_agents = [
                destination_agent.name,
                flight_agent.name,
                hotel_agent.name,
                activity_agent.name,
                safety_agent.name,
                budget_agent.name,
                final_planner_agent.name,
            ]
            assert call_records == expected_agents, f"Agent invocation order mismatch: {call_records} vs {expected_agents}"

            # 3. Verify final plan was produced in state
            assert "final_plan" in result
            assert "Mocked output for Final Travel Planner" in result["final_plan"]

    asyncio.run(_run())


def test_trip_request_state_flow():
    """Verify state propagation across all nodes in the pipeline."""
    async def _run():
        responses = {
            destination_agent.name: "Destination: Goa is great for beaches.",
            flight_agent.name: "Flight: Recommended flight HYD-GOI.",
            hotel_agent.name: "Hotel: Stay near Calangute.",
            activity_agent.name: "Activity: Water sports and beach walks.",
            safety_agent.name: "Safety: Keep hydrated and watch beach flags.",
            budget_agent.name: "Budget: Trip fits within ₹30,000 budget.",
            final_planner_agent.name: "# 4-Day Goa Itinerary\nComplete travel plan."
        }

        async def mock_runner_run(agent, prompt, *args, **kwargs):
            agent_name = getattr(agent, "name", str(agent))
            return MockAgentRunResult(responses.get(agent_name, "Default mock"))

        with patch("agents.Runner.run", side_effect=mock_runner_run), \
             patch("backend.graph.safety_node.get_weather", return_value={"current": {}, "daily": {}}):

            initial_state = {
                "user_request": "Plan a 4 day trip to Goa under ₹30,000"
            }

            result = await travel_graph.ainvoke(initial_state)

            assert "destination_result" in result
            assert "flight_result" in result
            assert "hotel_result" in result
            assert "activity_result" in result
            assert "safety_result" in result
            assert "budget_result" in result
            assert "final_plan" in result
            assert result["final_plan"] == "# 4-Day Goa Itinerary\nComplete travel plan."

    asyncio.run(_run())


def test_fastapi_plan_endpoint_with_mocked_graph(client):
    """Verify that the FastAPI endpoint /plan returns 200 with the final plan."""
    mock_plan_text = "# Complete 4-Day Goa Plan\nEnjoy your trip!"

    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.return_value = {"final_plan": mock_plan_text}

        response = client.post("/plan", json={"request": "Plan a trip to Goa"})

        assert response.status_code == 200
        data = response.json()
        assert data["plan"] == mock_plan_text


def test_fastapi_plan_endpoint_handles_429_quota_exhaustion(client):
    """Verify that Gemini 429 quota exhaustion is caught and returned with clean 429 JSON."""
    mock_error = openai.RateLimitError(
        message="RESOURCE_EXHAUSTED: You have exhausted your quota",
        response=AsyncMock(status_code=429),
        body={"error": {"code": 429, "status": "RESOURCE_EXHAUSTED"}}
    )

    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.side_effect = mock_error

        response = client.post("/plan", json={"request": "Plan a trip to Goa"})

        assert response.status_code == 429
        data = response.json()
        assert data["error"] == "RESOURCE_EXHAUSTED"
        assert data["detail"] == QUOTA_ERROR_MESSAGE
