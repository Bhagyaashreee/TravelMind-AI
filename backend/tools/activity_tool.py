
def search_activities(
    destination: str,
    interests: list[str] | None = None,
    max_results: int = 5,
):
    """
    Safe activity-search fallback for TravelMind AI.

    No live activity API is connected yet.
    Never invent prices, schedules, or availability.
    """

    return {
        "status": "search_not_available",
        "destination": destination,
        "interests": interests or [],
        "max_results": max_results,
        "activities": [],
        "message": (
            "Live activity data is not currently available. "
            "General activity suggestions may be provided, but "
            "prices, schedules, and availability are unverified."
        ),
    }
