import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

# Load environment variables from .env file
load_dotenv()

# Tracing disabled
set_tracing_disabled(True)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # We don't raise immediately to allow importing, but it will fail on generation
    print("WARNING: GEMINI_API_KEY environment variable is not set. Please obtain a free API key from Google AI Studio and set it in your .env file.")

# ==========================================
# Gemini connection via OpenAI compatible endpoint
# ==========================================
gemini_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key or "missing_key",
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-3.5-flash-lite",
    openai_client=gemini_client,
)

# Re-exporting for compatibility with existing agents
llama_model = gemini_model
qwen_model = gemini_model
gemma_model = gemini_model 