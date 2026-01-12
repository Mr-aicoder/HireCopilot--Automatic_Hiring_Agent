from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm

def get_inclusivity_knowledge():
    with open("rag_source/inclusivity_knowledge_base.md", "r") as f:
        return f.read()

def inclusivity_agent_node(state):
    """
    Reviews the draft JD for inclusivity and tone, suggesting improvements. (RAG)
    """
    print("---AGENT: Reviewing JD for inclusivity and tone---")
    draft_jd = state['draft_jd']
    llm = get_llm()
    knowledge_base = get_inclusivity_knowledge()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
            You are a Diversity, Equity, and Inclusion (DEI) expert. Review a draft job description using the provided knowledge base to make it more inclusive and welcoming.
            
            **Knowledge Base:**
            ---
            {knowledge_base}
            ---
            
            Rewrite the job description to remove biased language. After the rewritten JD, add a "Revisions Summary" section explaining your changes and why, referencing the knowledge base.
            """),
            ("human", "Please review and rewrite this job description:\n\n{draft_jd}")
        ]
    )

    chain = prompt | llm
    revised_jd_with_summary = chain.invoke({
        "draft_jd": draft_jd,
        "knowledge_base": knowledge_base
    }).content


    return {"final_jd": revised_jd_with_summary}


