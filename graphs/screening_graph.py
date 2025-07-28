from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from utils.output_parsers import ParsedResume, ScreenedCandidate

# Import agent nodes
from agents.resume_parser_agent import resume_parsing_agent_node
from agents.screening_agent import screening_agent_node

class ScreeningGraphState(TypedDict):
    """Represents the state of our resume screening graph."""
    resume_path: str
    final_jd: str
    candidate_name: Optional[str] = None
    parsed_resume: Optional[ParsedResume] = None
    screened_candidate: Optional[ScreenedCandidate] = None

def create_screening_graph():
    """
    Creates the LangGraph graph for screening a single resume.
    """
    workflow = StateGraph(ScreeningGraphState)

    # Define the nodes
    workflow.add_node("parse_resume", resume_parsing_agent_node)
    workflow.add_node("screen_candidate", screening_agent_node)

    # Define the edges
    workflow.set_entry_point("parse_resume")
    workflow.add_edge("parse_resume", "screen_candidate")
    workflow.add_edge("screen_candidate", END)

    # Compile the graph
    screening_graph = workflow.compile()
    return screening_graph