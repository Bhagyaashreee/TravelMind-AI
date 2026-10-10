from backend.tools.budget_tool import calculate_budget


result = calculate_budget(
    total_budget=30000,
    flights=2000,
    accommodation=5000,
    food=2000,
    transportation=1000,
    activities=3000,
    emergency=1000
)

print("\n💰 BUDGET CALCULATOR RESULT")
print("=" * 60)

print("Total Budget:", result["total_budget"])
print("Estimated Total:", result["estimated_total"])
print("Remaining/Excess:", result["remaining_or_excess"])
print("Status:", result["status"])

print("\nBreakdown:")
for category, amount in result["breakdown"].items():
    print(f"{category}: ₹{amount}")