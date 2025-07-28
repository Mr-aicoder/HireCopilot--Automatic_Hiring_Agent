from pydantic import BaseModel, Field
from typing import List
from typing import List, Optional

class JobDescriptionResearch(BaseModel):
    """Structured output for market research on job descriptions."""
    common_responsibilities: List[str] = Field(description="List of common responsibilities found in similar roles.")
    common_qualifications: List[str] = Field(description="List of common qualifications and skills required.")
    tech_stacks: List[str] = Field(description="List of common technologies and tools mentioned.")

class ParsedResume(BaseModel):
    """Structured output for a parsed resume."""
    full_name: str = Field(description="Candidate's full name.")
    email:Optional[str] = Field(description="Candidate's email address.", default=None) 
    phone_number: Optional[str] = Field(default=None, description="Candidate's phone number, if available.")
    skills: List[str] = Field(description="List of key technical and soft skills.")
    work_experience_summary: str = Field(description="A brief summary of the candidate's work experience.")
    education_summary: str = Field(description="A brief summary of the candidate's education.")

class ScreenedCandidate(BaseModel):
    """Structured output for a screened candidate."""
    score: int = Field(description="A score from 0 to 100 representing the candidate's fit for the role.")
    rationale: str = Field(description="A detailed explanation for the score, highlighting how the candidate's experience aligns with the job description.")
    strengths: List[str] = Field(description="Key strengths of the candidate relevant to the role.")
    weaknesses: List[str] = Field(description="Areas where the candidate may not meet the requirements or has less experience.")

class GeneratedInterviewQuestions(BaseModel):
    """Structured output for tailored interview questions."""
    technical_questions: List[str] = Field(description="List of technical questions tailored to the candidate's skills and the job requirements.")
    behavioral_questions: List[str] = Field(description="List of behavioral questions to assess teamwork, problem-solving, and past experiences.")
    situational_questions: List[str] = Field(description="List of situational questions, often related to addressing gaps or weaknesses constructively.")


