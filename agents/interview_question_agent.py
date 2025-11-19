from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utils.llm_provider import get_llm
from utils.output_parsers import GeneratedInterviewQuestions # We will create this next

def generate_interview_questions(final_jd: str, screened_candidate_details: dict, candidate_name: str):
    """
    Generates tailored interview questions based on a candidate's profile and the job description.
    This is called on-demand, not as part of a graph.
    """
    print(f"---AGENT: Generating interview questions for {candidate_name}---")
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=GeneratedInterviewQuestions)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert Senior Hiring Manager and an elite interviewer. Your task is to generate a set of tailored interview questions for a candidate based on their resume and how they stack up against a specific job description.

        Analyze the provided Job Description, the candidate's screening report (strengths and weaknesses), and generate insightful questions.

        - **Technical Questions:** Probe deeper into their stated strengths and required tech stack.
        - **Behavioral Questions:** Based on their experience, ask questions to understand how they operate in a team (e.g., STAR method questions).
        - **Situational Questions:** Explore the areas listed as "weaknesses" or "gaps" in a constructive way. Frame these to understand their problem-solving skills and willingness to learn, not to corner them. For example, if they lack a specific technology, ask how they would approach learning it for a project.
        
        Provide a structured list of questions using the requested JSON format.
        """),
        ("human", """
        **JOB DESCRIPTION:**
        ---
        {final_jd}
        ---

        **CANDIDATE SCREENING REPORT for {candidate_name}:**
        ---
        - Strengths: {strengths}
        - Weaknesses/Gaps: {weaknesses}
        - Rationale: {rationale}
        ---
        
        Please generate a set of interview questions for {candidate_name}.

        {format_instructions}
        """)
    ])

    chain = prompt | llm | parser

    questions = chain.invoke({
        "final_jd": final_jd,
        "candidate_name": candidate_name,
        "strengths": ", ".join(screened_candidate_details.strengths),
        "weaknesses": ", ".join(screened_candidate_details.weaknesses),
        "rationale": screened_candidate_details.rationale,
        "format_instructions": parser.get_format_instructions()
    })


    return questions
