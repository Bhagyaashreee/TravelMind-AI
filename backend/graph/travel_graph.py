from langgraph.graph import StateGraph, START, END

from backend.graph.state import TravelState
from backend.graph.destination_node import destination_node
from backend.graph.flight_node import flight_node
from backend.graph.hotel_node import hotel_node
from backend.graph.activity_node import activity_node
from backend.graph.safety_node import safety_node
from backend.graph.budget_node import budget_node
from backend.graph.final_planner_node import final_planner_node


builder = StateGraph(TravelState)

builder.add_node("destination", destination_node)
builder.add_node("flight", flight_node)
builder.add_node("hotel", hotel_node)
builder.add_node("activity", activity_node)
builder.add_node("safety", safety_node)
builder.add_node("budget", budget_node)
builder.add_node("final_planner", final_planner_node)

builder.add_edge(START, "destination")
builder.add_edge("destination", "flight")
builder.add_edge("flight", "hotel")
builder.add_edge("hotel", "activity")
builder.add_edge("activity", "safety")
builder.add_edge("safety", "budget")
builder.add_edge("budget", "final_planner")
builder.add_edge("final_planner", END)

travel_graph = builder.compile()