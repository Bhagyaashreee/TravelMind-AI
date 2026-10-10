
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    max_results: int = 5,
):
    """
    Return clearly labelled demo flight data for local testing.

    These values are fictional and must never be treated as
    real flight schedules, availability, or booking prices.
    """

    return {
        "status": "demo_data",
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "flights": [],
        "message": (
            "Demo mode is enabled. No verified flight prices or "
            "availability are available. No real flight search "
            "has been performed."
        ),
    }
