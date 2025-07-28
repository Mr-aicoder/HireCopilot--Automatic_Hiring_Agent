from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from utils.output_parsers import JobDescriptionResearch

# Import agent nodes
from agents.market_research_agent import research_agent_node
from agents.jd_crafter_agent import jd_crafting_agent_node
from agents.inclusivity_agent import inclusivity_agent_node

class JDGraphState(TypedDict):
    """Represents the state of our JD generation graph."""
    job_title: str
    research_findings: Optional[JobDescriptionResearch] = None
    draft_jd: Optional[str] = None
    final_jd: Optional[str] = None

def create_jd_graph():
    """
    Creates the LangGraph graph for generating a job description.
    """
    workflow = StateGraph(JDGraphState)

    # Define the nodes
    workflow.add_node("market_research", research_agent_node)
    workflow.add_node("jd_crafter", jd_crafting_agent_node)
    workflow.add_node("inclusivity_review", inclusivity_agent_node)

    # Define the edges
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "jd_crafter")
    workflow.add_edge("jd_crafter", "inclusivity_review")
    workflow.add_edge("inclusivity_review", END)

    # Compile the graph
    jd_graph = workflow.compile()
    return jd_graph