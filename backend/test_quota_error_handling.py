import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import openai

from backend.main import app, QUOTA_ERROR_MESSAGE


@pytest.fixture
def client():
    return TestClient(app)


def test_plan_endpoint_openai_ratelimit_error(client):
    """Verify that an openai.RateLimitError returns HTTP 429 with clear JSON message."""
    mock_rate_limit_error = openai.RateLimitError(
        message="RESOURCE_EXHAUSTED: quota exceeded",
        response=AsyncMock(status_code=429),
        body={
            "error": {
                "message": "Resource has been exhausted (e.g. check quota).",
                "type": "RESOURCE_EXHAUSTED",
                "code": 429,
            }
        },
    )

    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.side_effect = mock_rate_limit_error

        response = client.post("/plan", json={"request": "Plan a 3-day trip to Goa"})

        assert response.status_code == 429
        data = response.json()
        assert "detail" in data
        assert data["detail"] == QUOTA_ERROR_MESSAGE
        assert data["error"] == "RESOURCE_EXHAUSTED"
        assert "Gemini API request quota has been exhausted" in data["detail"]


def test_plan_endpoint_generic_quota_exception(client):
    """Verify that a generic exception mentioning RESOURCE_EXHAUSTED returns HTTP 429."""
    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.side_effect = RuntimeError("429 RESOURCE_EXHAUSTED quota exceeded for model gemini-3.6-flash")

        response = client.post("/plan", json={"request": "Plan a 3-day trip to Goa"})

        assert response.status_code == 429
        data = response.json()
        assert data["detail"] == QUOTA_ERROR_MESSAGE
        assert data["error"] == "RESOURCE_EXHAUSTED"


def test_plan_endpoint_success_mocked(client):
    """Verify that successful execution returns HTTP 200 with the plan."""
    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.return_value = {
            "final_plan": "Mocked travel itinerary for Goa."
        }

        response = client.post("/plan", json={"request": "Plan a 3-day trip to Goa"})

        assert response.status_code == 200
        data = response.json()
        assert data["plan"] == "Mocked travel itinerary for Goa."


def test_plan_endpoint_unrelated_internal_error(client):
    """Verify that an unrelated error returns HTTP 500 JSON without crashing."""
    with patch("backend.main.travel_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.side_effect = ValueError("Some unexpected internal error")

        response = client.post("/plan", json={"request": "Plan a 3-day trip to Goa"})

        assert response.status_code == 500
        data = response.json()
        assert "An error occurred while generating the plan" in data["detail"]
        assert data["error"] == "INTERNAL_SERVER_ERROR"
