import asyncio

from agents import Agent, Runner

from backend.models.model_config import (
    llama_model,
    qwen_model,
    gemma_model,
)


async def test_model(name, model):

    agent = Agent(
        name=name,
        instructions=f"""
        You are the {name}.

        Answer the user's question briefly.
        """,
        model=model,
    )

    result = await Runner.run(
        agent,
        "Tell me one interesting fact about Goa."
    )

    print(f"\n{'=' * 50}")
    print(f"{name}")
    print(f"{'=' * 50}")
    print(result.final_output)


async def main():

    await test_model(
        "Llama Travel Agent",
        llama_model
    )

    await test_model(
        "Qwen Travel Agent",
        qwen_model
    )

    await test_model(
        "Gemma Travel Agent",
        gemma_model
    )


if __name__ == "__main__":
    asyncio.run(main())