def calculate_budget(
    total_budget,
    flights=0,
    accommodation=0,
    food=0,
    transportation=0,
    activities=0,
    emergency=0
):
    """
    Calculate the total trip cost and compare it
    with the user's total budget.
    """

    estimated_total = (
        flights
        + accommodation
        + food
        + transportation
        + activities
        + emergency
    )

    difference = total_budget - estimated_total

    if difference > 0:
        status = "within_budget"
    elif difference < 0:
        status = "over_budget"
    else:
        status = "exactly_matches_budget"

    return {
        "total_budget": total_budget,
        "estimated_total": estimated_total,
        "remaining_or_excess": abs(difference),
        "status": status,
        "breakdown": {
            "flights": flights,
            "accommodation": accommodation,
            "food": food,
            "transportation": transportation,
            "activities": activities,
            "emergency": emergency
        }
    }