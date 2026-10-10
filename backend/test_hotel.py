from backend.tools.hotel_tool import search_hotels


result = search_hotels(
    destination="Goa, India",
    check_in="2026-10-15",
    check_out="2026-10-19",
    travelers=2
)

print("\n🏨 HOTEL SEARCH RESULT")
print("=" * 60)
print(result)