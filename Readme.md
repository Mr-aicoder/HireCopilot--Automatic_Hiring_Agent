# HireFlow: Automatic Hiring Agent
This is a multi-agent AI application built with Streamlit, LangGraph, and LangChain to automate the hiring process.

https://github.com/user-attachments/assets/ce4b2060-5e82-4633-b377-01cbd234437e

## Features

- **Phase 1: Job Description Generation**
  - Takes a simple job title (e.g., "Senior Backend Engineer, Python/AWS").
  - A Market Research Agent finds similar JDs online.
  - A JD Crafter Agent synthesizes the research into a first draft.
  - An Inclusivity & Tone Agent refines the draft using a RAG knowledge base to ensure fair and effective language.

- **Phase 2: Candidate Screening**
  - Upload multiple candidate resumes (PDFs).
  - A Resume Parser Agent extracts key information into a structured format.
  - A Screening & Scoring Agent compares each resume against the generated JD, providing a score and detailed rationale.
  - A Summarizer Agent creates a concise summary for the top candidates.
 
- **Phase 3: Interview Preparation**
  - After screening, select a high-scoring candidate from a dropdown list.
  - An **Interview Question Generator** agent analyzes the specific candidate's profile against the job description.
  - It generates a tailored set of interview questions covering **technical, behavioral, and situational** aspects, designed to probe the candidate's unique strengths and explore any identified gaps.
 
  

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
