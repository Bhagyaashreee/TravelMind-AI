def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    max_results: int = 5,
):
    """
    Flight search tool.
    Currently returns a safe fallback because live flight
    data is not connected yet.
    """

    return {
        "status": "search_not_available",
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "flights": [],
        "message": (
            "Live flight data is not currently available. "
            "Do not invent flight prices, schedules, or availability."
        ),
    }

