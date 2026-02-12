from langgraph.graph import StateGraph
from app.schemas import CareerState
from app.graph import cv_node, job_node, llm_match_node



def build_graph():

    builder = StateGraph(CareerState)

    # Add nodes
    builder.add_node("cv_node", cv_node)
    builder.add_node("job_node", job_node)
    builder.add_node("llm_match_node", llm_match_node)

    # Entry point
    builder.set_entry_point("cv_node")
    builder.add_edge("cv_node", "job_node")
    
    builder.add_edge("job_node", "llm_match_node")  

    # Finish
    builder.set_finish_point("llm_match_node")

    return builder.compile()
