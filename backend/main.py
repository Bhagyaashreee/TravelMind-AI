from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.graph.travel_graph import travel_graph


app = FastAPI(
    title="TravelMind AI",
    description="Multi-Agent Personalized Travel Planner",
    version="1.0.0"
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

    result = await travel_graph.ainvoke(initial_state)

    return {
        "plan": result.get(
            "final_plan",
            "No travel plan generated."
        )
    }