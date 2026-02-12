from langgraph.graph import StateGraph
from app.schemas import CareerState
from app.graph import cv_node


def build_graph():

    builder = StateGraph(CareerState)

    # Add nodes
    builder.add_node("cv_node", cv_node)

    # Entry point
    builder.set_entry_point("cv_node")

    # Finish
    builder.set_finish_point("cv_node")

    return builder.compile()
