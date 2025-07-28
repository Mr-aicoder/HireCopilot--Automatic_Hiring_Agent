import os

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def get_llm():
    """Initializes and returns the ChatOpenAI model."""
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY set this envirnment variable to use Groq LLMs")
    
    # Using gpt-4o-mini as a powerful and cost-effective model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0,
        convert_system_message_to_human=True 
    )
    return llm

