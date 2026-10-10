
from typing import TypedDict, Any


class TravelState(TypedDict, total=False):
    # Original user request
    user_request: str

    # Agent results
    destination_result: str
    flight_result: str
    hotel_result: str
    activity_result: str
    safety_result: str
    budget_result: str

    # Structured tool data
    flight_data: dict[str, Any]
    hotel_data: dict[str, Any]
    activity_data: dict[str, Any]

    # Flight, hotel and activity data status
    live_flight_data: bool
    demo_flight_data: bool
    live_hotel_data: bool
    live_activity_data: bool

    # Structured budget information
    total_budget: float

    flight_cost: float
    hotel_cost: float
    food_cost: float
    transportation_cost: float
    activity_cost: float
    emergency_cost: float

    # Final calculated budget
    estimated_total: float
    remaining_budget: float
    budget_status: str

    # Final output
    final_plan: str
