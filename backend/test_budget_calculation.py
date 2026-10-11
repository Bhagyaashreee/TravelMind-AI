import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from backend.tools.budget_tool import calculate_budget, estimate_trip_budget
from backend.graph.budget_node import budget_node, extract_budget, extract_travelers, extract_duration


def test_calculate_budget_within_budget():
    """Verify that calculate_budget accurately calculates all 6 categories and handles surplus."""
    res = calculate_budget(
        total_budget=30000,
        transportation=7000,
        accommodation=6000,
        food=6400,
        local_transport=3200,
        activities=3000,
        emergency=2500,
    )

    assert res["total_budget"] == 30000.0
    assert res["estimated_total"] == 28100.0
    assert res["remaining_budget"] == 1900.0
    assert res["difference"] == 1900.0
    assert res["status"] == "within_budget"
    assert res["fits_budget"] is True
    assert res["breakdown"]["transportation"] == 7000.0
    assert res["breakdown"]["accommodation"] == 6000.0
    assert res["breakdown"]["food"] == 6400.0
    assert res["breakdown"]["local_transport"] == 3200.0
    assert res["breakdown"]["activities"] == 3000.0
    assert res["breakdown"]["emergency"] == 2500.0


def test_calculate_budget_over_budget():
    """Verify that calculate_budget properly identifies when trip exceeds target budget."""
    res = calculate_budget(
        total_budget=20000,
        transportation=7000,
        accommodation=6000,
        food=6400,
        local_transport=3200,
        activities=3000,
        emergency=2500,
    )

    assert res["total_budget"] == 20000.0
    assert res["estimated_total"] == 28100.0
    assert res["remaining_budget"] == 0.0
    assert res["difference"] == -8100.0
    assert res["remaining_or_excess"] == 8100.0
    assert res["status"] == "over_budget"
    assert res["fits_budget"] is False


def test_calculate_budget_backwards_compatibility():
    """Verify backwards compatibility for legacy callers passing flights/transportation."""
    res = calculate_budget(
        total_budget=30000,
        flights=2000,
        accommodation=5000,
        food=2000,
        transportation=1000,
        activities=3000,
        emergency=1000,
    )

    assert res["estimated_total"] == 14000.0
    assert res["remaining_budget"] == 16000.0
    assert res["status"] == "within_budget"
    assert res["breakdown"]["flights"] == 2000.0
    assert res["breakdown"]["local_transport"] == 1000.0


def test_estimate_trip_budget_accounts_for_travelers_and_duration():
    """Verify that estimate_trip_budget scales with duration days and travelers."""
    # 2 travelers, 4 days (3 nights, 1 room)
    res_2t_4d = estimate_trip_budget(
        total_budget=30000,
        travelers=2,
        duration_days=4,
    )

    assumptions = res_2t_4d["assumptions"]
    assert assumptions["travelers"] == 2
    assert assumptions["duration_days"] == 4
    assert assumptions["nights"] == 3
    assert assumptions["rooms"] == 1
    assert assumptions["is_live_transport"] is False

    breakdown = res_2t_4d["breakdown"]
    # 3500 * 2 travelers = 7000
    assert breakdown["transportation"] == 7000.0
    # 2000 * 1 room * 3 nights = 6000
    assert breakdown["accommodation"] == 6000.0
    # 800 * 2 travelers * 4 days = 6400
    assert breakdown["food"] == 6400.0
    # 800 * 4 days = 3200
    assert breakdown["local_transport"] == 3200.0
    # 1200 * 2 travelers = 2400
    assert breakdown["activities"] == 2400.0
    # 10% contingency on subtotal (25000 * 0.10) = 2500
    assert breakdown["emergency"] == 2500.0
    assert res_2t_4d["estimated_total"] == 27500.0
    assert res_2t_4d["remaining_budget"] == 2500.0
    assert res_2t_4d["status"] == "within_budget"


def test_estimate_trip_budget_with_live_flight_cost():
    """Verify that live flight data overrides estimated transit and is marked as live data."""
    res = estimate_trip_budget(
        total_budget=35000,
        travelers=2,
        duration_days=3,
        live_flight_cost=4500.0,
    )

    assert res["assumptions"]["is_live_transport"] is True
    assert res["assumptions"]["transportation_type"] == "Verified Live Flight Data"
    assert res["breakdown"]["transportation"] == 9000.0  # 4500 * 2 travelers


def test_extract_parameters_and_assumptions():
    """Verify regex extraction of budget, duration, and travelers."""
    # Explicit request
    req1 = "Plan a 5 day trip from Hyderabad to Goa for 2 travelers under ₹30,000."
    assert extract_budget(req1) == 30000
    days1, days_explicit1 = extract_duration(req1)
    assert (days1, days_explicit1) == (5, True)
    trav1, trav_explicit1 = extract_travelers(req1)
    assert (trav1, trav_explicit1) == (2, True)

    # Missing parameters -> defaults with is_explicit=False
    req2 = "Plan a trip to Manali"
    assert extract_budget(req2) == 0
    days2, days_explicit2 = extract_duration(req2)
    assert (days2, days_explicit2) == (3, False)
    trav2, trav_explicit2 = extract_travelers(req2)
    assert (trav2, trav_explicit2) == (2, False)


def test_budget_node_populates_all_state_fields():
    """Verify that budget_node calculates estimates and updates TravelState completely."""
    async def _run():
        class MockResult:
            def __init__(self, text):
                self.final_output = text

        captured_prompt = []

        async def mock_run(agent, prompt, *args, **kwargs):
            captured_prompt.append(prompt)
            return MockResult("## Mocked Budget Agent Analysis\nTrip is within budget.")

        with patch("agents.Runner.run", side_effect=mock_run):
            state = {
                "user_request": "Plan a 4 day trip to Goa for 2 travelers under ₹30,000"
            }

            res = await budget_node(state)

            # Check that all state keys are populated
            assert "budget_result" in res
            assert res["total_budget"] == 30000.0
            assert res["flight_cost"] == 7000.0
            assert res["hotel_cost"] == 6000.0
            assert res["food_cost"] == 6400.0
            assert res["transportation_cost"] == 3200.0
            assert res["local_transport_cost"] == 3200.0
            assert res["activity_cost"] == 2400.0
            assert res["emergency_cost"] == 2500.0
            assert res["estimated_total"] == 27500.0
            assert res["remaining_budget"] == 2500.0
            assert res["budget_status"] == "within_budget"

            # Check prompt fed to LLM contains the 6 categories and assumptions
            prompt_text = captured_prompt[0]
            assert "Transportation (Intercity)" in prompt_text
            assert "Accommodation" in prompt_text
            assert "Food & Dining" in prompt_text
            assert "Local Transport" in prompt_text
            assert "Activities & Sightseeing" in prompt_text
            assert "Emergency Contingency Buffer" in prompt_text
            assert "within_budget" in prompt_text

    asyncio.run(_run())
