import asyncio

from agents import Runner
from backend.agents.budget_agent import budget_agent


async def main():

    prompt = """
I want to travel from Hyderabad to Goa.

Trip duration: 4 days
Travelers: 2
Total budget: ₹30,000

My interests are:
- beaches
- adventure
- nature
- nightlife

Live flight prices are NOT available.
Live hotel prices are NOT available.
Live activity prices are NOT available.

Analyze my budget and give me a practical budget plan.

Do not treat estimated prices as real prices.
Clearly label estimates.
"""

    print("\n💰 Running Budget Agent...")

    result = await Runner.run(
        budget_agent,
        prompt
    )

    print("\n" + "=" * 60)
    print("BUDGET AGENT RESULT")
    print("=" * 60)

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())