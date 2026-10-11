def calculate_budget(
    total_budget: float,
    transportation: float = 0,
    accommodation: float = 0,
    food: float = 0,
    local_transport: float = 0,
    activities: float = 0,
    emergency: float = 0,
    flights: float = 0,
) -> dict:
    """
    Calculate the total estimated trip cost and compare it with the user's total budget.

    Categories:
    - transportation: Intercity transit (flights, trains, intercity bus)
    - accommodation: Hotel, hostel, or resort stay
    - food: Meals, dining, and snacks
    - local_transport: Local travel (taxis, auto-rickshaws, scooter/car rentals)
    - activities: Sightseeing, entry tickets, and tours
    - emergency: Emergency contingency buffer

    Supports 'flights' parameter for backwards compatibility.
    """
    # Handle backwards compatibility where 'flights' was intercity transit and 'transportation' was local transport
    if flights > 0 and transportation > 0 and local_transport == 0:
        intercity_transport = float(flights)
        actual_local_transport = float(transportation)
    elif flights > 0 and transportation == 0:
        intercity_transport = float(flights)
        actual_local_transport = float(local_transport)
    else:
        intercity_transport = float(transportation)
        actual_local_transport = float(local_transport)

    accommodation_cost = float(accommodation)
    food_cost = float(food)
    activities_cost = float(activities)
    emergency_cost = float(emergency)
    budget_limit = float(total_budget) if total_budget else 0.0

    estimated_total = round(
        intercity_transport
        + accommodation_cost
        + food_cost
        + actual_local_transport
        + activities_cost
        + emergency_cost,
        2,
    )

    if budget_limit > 0:
        difference = round(budget_limit - estimated_total, 2)
        if difference > 0:
            status = "within_budget"
        elif difference < 0:
            status = "over_budget"
        else:
            status = "exactly_matches_budget"
        remaining_budget = max(0.0, difference)
        excess_or_deficit = abs(difference)
    else:
        difference = 0.0
        status = "baseline_estimate"
        remaining_budget = 0.0
        excess_or_deficit = 0.0

    return {
        "total_budget": budget_limit,
        "estimated_total": estimated_total,
        "remaining_budget": remaining_budget,
        "remaining_or_excess": excess_or_deficit,
        "difference": difference,
        "status": status,
        "fits_budget": (difference >= 0) if budget_limit > 0 else None,
        "breakdown": {
            "transportation": intercity_transport,
            "accommodation": accommodation_cost,
            "food": food_cost,
            "local_transport": actual_local_transport,
            "activities": activities_cost,
            "emergency": emergency_cost,
            # Backwards-compatibility aliases:
            "flights": intercity_transport,
        },
    }


def estimate_trip_budget(
    total_budget: float = 0,
    travelers: int = 2,
    duration_days: int = 3,
    live_flight_cost: float | None = None,
) -> dict:
    """
    Generate realistic, clearly labelled estimated budget baselines
    accounting for number of travelers and trip duration.

    Assumptions:
    - Accommodation: 1 standard room for every 2 travelers.
    - Duration: Nights = max(1, duration_days - 1).
    - Emergency buffer: ~10% of subtotal.
    """
    travelers_count = max(1, int(travelers))
    days = max(1, int(duration_days))
    nights = max(1, days - 1)
    rooms = max(1, (travelers_count + 1) // 2)

    # 1. Transportation (Intercity)
    if live_flight_cost is not None and live_flight_cost > 0:
        transportation_cost = round(float(live_flight_cost) * travelers_count, 2)
        transportation_label = "Verified Live Flight Data"
        is_live_transport = True
    else:
        # Standard estimated round-trip intercity transit baseline per traveler
        transportation_cost = round(3500.0 * travelers_count, 2)
        transportation_label = "Estimated Intercity Transit (~₹3,500/traveler)"
        is_live_transport = False

    # 2. Accommodation (~₹2,000 per room per night for standard stay)
    accommodation_cost = round(2000.0 * rooms * nights, 2)

    # 3. Food & Dining (~₹800 per traveler per day)
    food_cost = round(800.0 * travelers_count * days, 2)

    # 4. Local Transport (~₹800 per day for group: cabs, auto, scooter/car rental)
    local_transport_cost = round(800.0 * days, 2)

    # 5. Activities & Sightseeing (~₹1,200 per traveler)
    activities_cost = round(1200.0 * travelers_count, 2)

    # Subtotal before contingency
    subtotal = (
        transportation_cost
        + accommodation_cost
        + food_cost
        + local_transport_cost
        + activities_cost
    )

    # 6. Emergency Contingency (~10% buffer for unexpected expenses)
    emergency_cost = round(max(1000.0, subtotal * 0.10), 2)

    calc = calculate_budget(
        total_budget=total_budget,
        transportation=transportation_cost,
        accommodation=accommodation_cost,
        food=food_cost,
        local_transport=local_transport_cost,
        activities=activities_cost,
        emergency=emergency_cost,
    )

    calc["assumptions"] = {
        "travelers": travelers_count,
        "duration_days": days,
        "nights": nights,
        "rooms": rooms,
        "room_sharing": f"{rooms} room(s) for {travelers_count} traveler(s)",
        "transportation_type": transportation_label,
        "is_live_transport": is_live_transport,
    }

    return calc