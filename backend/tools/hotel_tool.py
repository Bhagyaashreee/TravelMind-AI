def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    travelers: int = 2,
    max_results: int = 5
):
    """
    Hotel search tool.

    Currently returns a safe fallback because live hotel
    data is not connected yet.

    The system must never invent hotel prices or availability.
    """

    return {
        "status": "search_not_available",
        "destination": destination,
        "check_in": check_in,
        "check_out": check_out,
        "travelers": travelers,
        "max_results": max_results,
        "message": (
            "Live hotel data is not currently available. "
            "Do not invent hotel prices, ratings, or availability."
        )
    }