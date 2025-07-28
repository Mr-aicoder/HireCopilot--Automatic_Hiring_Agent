from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm

def jd_crafting_agent_node(state):
    """
    Takes research findings and synthesizes them into a draft job description.
    """
    print("---AGENT: Crafting first draft of JD---")
    research_findings = state['research_findings']
    job_title = state['job_title']
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert HR copywriter. Create a comprehensive job description based on the provided research. Use Markdown for formatting."),
            ("human", """
            Draft a job description for: **{job_title}**.

            Use the following research:
            **Common Responsibilities:**
            {responsibilities}
            **Common Qualifications & Skills:**
            {qualifications}
            **Common Tech Stacks:**
            {tech_stacks}

            Structure the JD with: Job Title, Company Intro (placeholder), Role Overview, Key Responsibilities, Required Qualifications, and Preferred Qualifications.
            """)
        ]
    )

    chain = prompt | llm
    draft_jd = chain.invoke({
        "job_title": job_title,
        "responsibilities": "\n- ".join(research_findings.common_responsibilities),
        "qualifications": "\n- ".join(research_findings.common_qualifications),
        "tech_stacks": ", ".join(research_findings.tech_stacks)
    }).content

    return {"draft_jd": draft_jd}