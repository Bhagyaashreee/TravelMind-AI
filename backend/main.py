import sys
import openai
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Force UTF-8 encoding for standard output to prevent Windows charmap crashes on emojis
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.graph.travel_graph import travel_graph


app = FastAPI(
    title="TravelMind AI",
    description="Multi-Agent Personalized Travel Planner",
    version="1.0.0"
)

QUOTA_ERROR_MESSAGE = (
    "The Gemini API request quota has been exhausted (HTTP 429: RESOURCE_EXHAUSTED). "
    "The free-tier limit for Gemini has been reached. "
    "Please wait a few moments before trying again or check your Google AI Studio quota."
)


def is_gemini_quota_error(exc: BaseException) -> bool:
    """Check if an exception is caused by Gemini/OpenAI rate limit or quota exhaustion."""
    curr = exc
    while curr is not None:
        if isinstance(curr, openai.RateLimitError):
            return True
        if getattr(curr, "status_code", None) == 429:
            return True
        resp = getattr(curr, "response", None)
        if resp is not None and getattr(resp, "status_code", None) == 429:
            return True
        msg = str(curr).lower()
        if any(term in msg for term in ("resource_exhausted", "quota", "429", "rate limit", "rate_limit")):
            return True
        curr = getattr(curr, "__cause__", None) or getattr(curr, "__context__", None)
    return False


@app.exception_handler(openai.RateLimitError)
async def rate_limit_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": QUOTA_ERROR_MESSAGE,
            "message": QUOTA_ERROR_MESSAGE,
            "error": "RESOURCE_EXHAUSTED"
        }
    )


# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class TravelRequest(BaseModel):
    request: str


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "TravelMind AI backend is running!"
    }


# ---------------------------------------------------------
# TRAVEL PLAN ENDPOINT
# ---------------------------------------------------------

@app.post("/plan")
async def create_travel_plan(data: TravelRequest):

    initial_state = {
        "user_request": data.request
    }

    try:
        result = await travel_graph.ainvoke(initial_state)
        return {
            "plan": result.get(
                "final_plan",
                "No travel plan generated."
            )
        }
    except openai.RateLimitError:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": QUOTA_ERROR_MESSAGE,
                "message": QUOTA_ERROR_MESSAGE,
                "error": "RESOURCE_EXHAUSTED"
            }
        )
    except Exception as exc:
        if is_gemini_quota_error(exc):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": QUOTA_ERROR_MESSAGE,
                    "message": QUOTA_ERROR_MESSAGE,
                    "error": "RESOURCE_EXHAUSTED"
                }
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": f"An error occurred while generating the plan: {str(exc)}",
                "message": f"An error occurred while generating the plan: {str(exc)}",
                "error": "INTERNAL_SERVER_ERROR"
            }
        )