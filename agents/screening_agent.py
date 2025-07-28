from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utils.llm_provider import get_llm
from utils.output_parsers import ScreenedCandidate

def screening_agent_node(state):
    """
    Compares a parsed resume against the job description to score and analyze the candidate. (RAG)
    """
    print(f"---AGENT: Screening candidate {state['candidate_name']}---")
    parsed_resume = state['parsed_resume']
    final_jd = state['final_jd']
    llm = get_llm()
    
    parser = PydanticOutputParser(pydantic_object=ScreenedCandidate)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
            You are an expert Technical Recruiter. Your task is to screen a candidate's resume against a job description. 
            Provide a score from 0-100 on their fit. 
            Justify the score with a detailed rationale, and list their key strengths and weaknesses based ONLY on the information in the resume and the job description.
            Use the provided JSON format for your response.
            """),
            ("human", """
            **JOB DESCRIPTION:**
            ---
            {final_jd}
            ---

            **CANDIDATE'S PARSED RESUME:**
            ---
            Full Name: {candidate_name}
            Email: {email}
            Skills: {skills}
            Work Experience: {work_experience}
            Education: {education}
            ---

            {format_instructions}
            """)
        ]
    )
    chain = prompt | llm | parser
    screened_candidate = chain.invoke({
        "final_jd": final_jd,
        "candidate_name": parsed_resume.full_name,
        "email": parsed_resume.email,
        "skills": ", ".join(parsed_resume.skills),
        "work_experience": parsed_resume.work_experience_summary,
        "education": parsed_resume.education_summary,
        "format_instructions": parser.get_format_instructions()
    })

    return {"screened_candidate": screened_candidate}