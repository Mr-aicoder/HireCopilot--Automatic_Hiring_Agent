import os
from pypdf import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utils.llm_provider import get_llm
from utils.output_parsers import ParsedResume

def resume_parsing_agent_node(state):
    """
    Parses a resume PDF to extract key information into a structured JSON format.
    """
    print("---AGENT: Parsing resume---")
    resume_path = state['resume_path']
    llm = get_llm()
    
    reader = PdfReader(resume_path)
    resume_text = "".join(page.extract_text() or "" for page in reader.pages)
        
    os.remove(resume_path) # Clean up the temporary file

    parser = PydanticOutputParser(pydantic_object=ParsedResume)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert resume parser. Extract key information from the resume text and structure it into a JSON object using the provided format."),
            ("human", "Parse the following resume text:\n\n{resume_text}\n\n{format_instructions}")
        ]
    )
    chain = prompt | llm | parser
    parsed_resume = chain.invoke({
        "resume_text": resume_text,
        "format_instructions": parser.get_format_instructions(),
    })

    return {"parsed_resume": parsed_resume, "candidate_name": parsed_resume.full_name}