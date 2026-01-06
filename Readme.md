# HireCopilot: Automatic Hiring Agent
This is a multi-agent AI application built with Streamlit, LangGraph, and LangChain to automate the complete hiring process.

https://github.com/user-attachments/assets/ce4b2060-5e82-4633-b377-01cbd234437e



# Features

## Phase 1: Job Description (JD) Generation. 
This phase is orchestrated by a LangGraph workflow that automatically creates a
comprehensive and inclusive job description from a simple job title
#### 1. Market Research: 
The research_agent_node (market_research_agent.py) is the 
entry point. It uses a web search tool (DuckDuckGo) to find similar job 
descriptions and then uses a Large Language Model (LLM) to extract and structure 
key information like common responsibilities, qualifications, and tech stacks.
#### 2. JD Crafting: 
The jd_crafting_agent_node (jd_crafter_agent.py) receives the 
research findings and acts as an "expert HR copywriter". It synthesizes the 
information into a draft job description using Markdown formatting, including 
sections like "Key Responsibilities" and "Required Qualifications". 
#### 3. Inclusivity Review: 
The inclusivity_agent_node (inclusivity_agent.py) takes the 
draft JD and acts as a "Diversity, Equity, and Inclusion (DEI) expert". It uses a 
Retrieval-Augmented Generation (RAG) approach by referencing a local 
markdown file containing best practices for inclusive language. The final JD, along 
with a "Revisions Summary," is then returned.

## Phase 2: Candidate Screening 
This phase screens uploaded resumes against the finalized job description. It is a 
separate LangGraph workflow. 
#### 1. Resume Parsing: 
The resume_parsing_agent_node (resume_parser_agent.py) 
takes a PDF resume file. It uses the pypdf library to extract the text from the PDF 
and then uses an LLM to parse it into a structured ParsedResume object 
containing the candidate's name, email, skills, and work experience. 
#### 2. Candidate Screening: 
The screening_agent_node (screening_agent.py) receives 
the parsed resume and the final JD. It acts as an "expert Technical Recruiter" to 
score the candidate from 0-100 on their fit. It provides a detailed rationale, as well 
as a list of strengths and weaknesses based only on the provided resume and JD. 
#### 3. Summarization: 
After all resumes are screened, the summarizer_agent 
(summerizer_agent.py) creates a concise "Hiring Manager's Briefing" by 
generating a 2-3 sentence summary for each of the top-scoring candidates. This 
summary highlights their relevance, strengths, and overall fit for the role.

## Phase 3: Interview Preparation 
This phase is handled on-demand and is not part of a LangGraph workflow. 
• The generate_interview_questions function (interview_question_agent.py) takes 
the final JD and the Screened_Candidate details for a selected candidate. 
• It acts as an "expert Senior Hiring Manager" to generate three types of questions: 
technical, behavioural, and situational. The situational questions are specifically 
designed to constructively explore weaknesses or gaps identified during 
screening. 
• The output is a structured Generated_Interview_Questions object, which is then 
displayed to the user.

<img width="1726" height="596" alt="Automatic Hiring Agent Diagram" src="https://github.com/user-attachments/assets/1e08ec58-22a5-4061-b82d-76b4d74eabd8" />

## Setup

1.  **Clone the repository.**

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    - Create a file named `.env` in the root directory.
    - Add your OpenAI API key to the `.env` file:
        GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    

5.  **Create an `uploads` directory:**
    ```bash
    mkdir uploads
    ```

    

## How to Run

Execute the Streamlit application from your terminal:

```bash
streamlit run app.py
```

Navigate to the local URL provided by Streamlit in your web browser.











