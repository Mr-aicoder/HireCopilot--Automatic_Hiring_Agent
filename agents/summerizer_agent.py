from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from typing import List, Dict

def summarizer_agent(top_candidates_data: List[Dict]):
    """
    Generates a 2-3 sentence summary for each of the top-scoring candidates.
    """
    print("---AGENT: Summarizing top candidates---")
    if not top_candidates_data:
        return "No candidates were processed or scored high enough to be summarized."
        
    llm = get_llm()

    # Format the candidate data into a string for the prompt
    candidates_info = ""
    for i, data in enumerate(top_candidates_data):
        candidate_name = data['candidate_name']
        score = data['screened_candidate'].score
        rationale = data['screened_candidate'].rationale
        candidates_info += f"Candidate {i+1}: {candidate_name}\nScore: {score}/100\nScreening Rationale: {rationale}\n\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert hiring manager's assistant. Your task is to write a concise "Hiring Manager's Briefing" based on the provided candidate screening results.
        
        For each candidate, provide a 2-3 sentence summary highlighting their relevance, key strengths, and overall fit for the role. 
        Start with a brief introductory sentence for the entire briefing.
        Structure the output clearly using Markdown.
        """),
        ("human", "Please create a briefing for the following top candidates:\n\n{candidates_info}")
    ])
    
    chain = prompt | llm
    summary = chain.invoke({"candidates_info": candidates_info}).content
    return summary