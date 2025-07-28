from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utils.llm_provider import get_llm
from utils.output_parsers import JobDescriptionResearch

def research_agent_node(state):
    """
    Uses web search to find similar job descriptions and extracts key info.
    This node is now fully fortified with error handling for network requests.
    """
    print("---AGENT: Researching similar job descriptions---")
    job_title = state['job_title']
    
    # Initialize search_results to a safe default value (empty string)
    search_results_text = ""
    try:
        search_tool = DuckDuckGoSearchRun()
        search_results_text = search_tool.run(f"job descriptions for '{job_title}' at top tech companies")
        print("---AGENT: Web search completed successfully.---")
    except Exception as e:
        print(f"\n--- WARNING: Web search failed in market_research_agent. Error: {e} ---\n")
        print("---AGENT: Continuing with no web search data. The JD will be generated from the LLM's general knowledge.---")

    try:
        llm = get_llm()
        parser = PydanticOutputParser(pydantic_object=JobDescriptionResearch)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert market researcher. Analyze the provided text from job descriptions to extract common responsibilities, qualifications, and tech stacks. If the text is empty, use your general knowledge to generate a plausible list for the given job title. Respond with a JSON object using the provided format."),
                ("human", "Analyze the following job description search results for '{job_title}':\n\n{search_results}\n\n{format_instructions}")
            ]
        )
        chain = prompt | llm | parser
        research_findings = chain.invoke({
            "job_title": job_title,
            "search_results": search_results_text[:8000],
            "format_instructions": parser.get_format_instructions(),
        })
        return {"research_findings": research_findings}
        
    except Exception as e:
        print(f"\n--- ERROR: LLM call failed in market_research_agent. Please check your API key. Error: {e} ---\n")
        empty_research = JobDescriptionResearch(common_responsibilities=[], common_qualifications=[], tech_stacks=[])
        return {"research_findings": empty_research}