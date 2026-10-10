from backend.tools.flight_tool import search_flights


result = search_flights(
    origin="HYD",
    destination="GOI",
    departure_date="2026-10-15"
)

print("\n✈️ FLIGHT SEARCH RESULT")
print("=" * 60)
print(result)