from openai import AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

# We are using Ollama locally,
# so OpenAI tracing is disabled.
set_tracing_disabled(True)


# ==========================================
# Ollama connection
# ==========================================

ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


# ==========================================
# MODEL 1 — Llama
# ==========================================

llama_model = OpenAIChatCompletionsModel(
    model="llama3.2:3b",
    openai_client=ollama_client,
)


# ==========================================
# MODEL 2 — Qwen
# ==========================================

qwen_model = OpenAIChatCompletionsModel(
    model="qwen2.5:3b",
    openai_client=ollama_client,
)


# ==========================================
# MODEL 3 — Gemma
# ==========================================

gemma_model = OpenAIChatCompletionsModel(
    model="gemma3:4b",
    openai_client=ollama_client,
)