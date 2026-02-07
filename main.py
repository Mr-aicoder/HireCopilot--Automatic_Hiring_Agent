import streamlit as st
import os
import uuid 
import utils.database as db 
from agents.interview_question_agent  import generate_interview_questions 
from graphs.jd_graph import  create_jd_graph
from graphs.screening_graph import  create_screening_graph
from agents.summerizer_agent import  summarizer_agent

# --- Page Configuration ---
st.set_page_config(
    page_title="HireCopilot | AI Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Initialize Database ---
db.init_db()

# --- Title and Description ---
st.title("🤖 HireCopilot")
st.markdown("Your AI-powered Hiring Assistant, now with a dedicated Interview Prep phase.")
st.info("Ensure your API key is set correctly in your `.env` file.")

# --- Initialize Session State ---
if "final_jd" not in st.session_state:
    st.session_state.final_jd = ""
if "screening_results" not in st.session_state:
    st.session_state.screening_results = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = {}
if "job_title_input" not in st.session_state:
    st.session_state.job_title_input = ""

# --- Create 'uploads' directory ---
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# --- UI Layout (Tabs) ---
tab1, tab2, tab3 = st.tabs([
    "**Phase 1: Job Description**",
    "**Phase 2: Candidate Screening**",
    "**Phase 3: Interview Prep**"
])

# =================================================================================================
# --- PHASE 1: JOB DESCRIPTION ---
# =================================================================================================
with tab1:
    st.header("Create or Load a Job Description")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        existing_jd_titles = [""] + db.load_jd_titles()
        selected_title = st.selectbox("Load an existing Job Description", options=existing_jd_titles, key="load_jd_select")
        if selected_title and st.button("Load Selected JD"):
            loaded_jd = db.get_jd_by_title(selected_title)
            if loaded_jd:
                st.session_state.final_jd = loaded_jd
                st.session_state.job_title_input = selected_title
                st.success(f"Loaded '{selected_title}' successfully.")

    st.subheader("Generate a New Job Description")
    st.session_state.job_title_input = st.text_input(
        "**Enter a job title to generate or update a JD**",
        value=st.session_state.job_title_input,
        placeholder="e.g., Senior Backend Engineer, Python/AWS"
    )

    if st.button("✨ Generate New JD", type="primary"):
        if st.session_state.job_title_input:
            with st.spinner("🚀 Launching agent team..."):
                result = None
                try:
                    jd_graph = create_jd_graph()
                    result = jd_graph.invoke({"job_title": st.session_state.job_title_input})
                except Exception as e:
                    st.error(f"An error occurred. Check terminal for logs. Error: {e}")
                if result and result.get('final_jd'):
                    st.session_state.final_jd = result['final_jd']
                    st.success("New Job Description generated!")
        else:
            st.error("Please enter a job title.")

    if st.session_state.final_jd:
        st.subheader("Edit & Finalize Job Description")
        edited_jd = st.text_area(
            "You can edit the JD below before screening or saving.",
            value=st.session_state.final_jd, height=400
        )
        st.session_state.final_jd = edited_jd

        col_save, col_download = st.columns(2)
        with col_save:
            if st.button("💾 Save Job Description", use_container_width=True):
                if st.session_state.job_title_input and st.session_state.final_jd:
                    db.save_jd(st.session_state.job_title_input, st.session_state.final_jd)
                    st.success(f"'{st.session_state.job_title_input}' saved to the database!")
                else:
                    st.warning("A job title and description are required to save.")
        with col_download:
             st.download_button("⬇️ Download JD as Markdown", data=st.session_state.final_jd,
                                file_name=f"{st.session_state.job_title_input.replace(' ', '_').lower()}_jd.md",
                                mime="text/markdown", use_container_width=True)

# =================================================================================================
# --- PHASE 2: CANDIDATE SCREENING ---
# =================================================================================================
with tab2:
    st.header("Screen Resumes Against Finalized JD")
    if not st.session_state.final_jd:
        st.warning("Please generate or load a Job Description in Phase 1.")
    else:
        with st.expander("View Job Description Used for Screening"):
            st.markdown(st.session_state.final_jd)
        
        uploaded_files = st.file_uploader(
            "Upload candidate resumes (PDFs only)", type="pdf", accept_multiple_files=True
        )

        if st.button("🕵️‍♂️ Screen All Resumes", type="primary", use_container_width=True):
            if uploaded_files:
                with st.spinner(f"🚀 Screening {len(uploaded_files)} resume(s)..."):
                    st.session_state.screening_results = None
                    st.session_state.interview_questions = {}
                    try:
                        uploads_dir = "uploads"
                        os.makedirs(uploads_dir, exist_ok=True)

                        
                        saved_files = []
                        for file in uploaded_files:
                            file_path = os.path.join("uploads", f"{uuid.uuid4()}_{file.name}")
                            with open(file_path, "wb") as f: f.write(file.getbuffer())
                            saved_files.append(file_path)

                        screening_graph = create_screening_graph()
                        screening_inputs = [{"resume_path": path, "final_jd": st.session_state.final_jd} for path in saved_files]
                        results = screening_graph.batch(screening_inputs)
                        st.session_state.screening_results = results
                        st.success("Screening complete! Check the results below and in the 'Interview Prep' tab.")
                    except Exception as e:
                        st.error(f"An error occurred during screening. Check terminal logs. Error: {e}")
            else:
                st.error("Please upload at least one resume.")

    if st.session_state.screening_results:
        successful_results = [res for res in st.session_state.screening_results if res and res.get('screened_candidate')]
        sorted_results = sorted(successful_results, key=lambda x: x['screened_candidate'].score, reverse=True)

        if sorted_results:
            st.subheader("🏆 Hiring Manager's Briefing")
            with st.spinner("Summarizing top candidates..."):
                summary = summarizer_agent(sorted_results[:3])
                st.markdown(summary)

        st.subheader("Detailed Screening Results")
        for result in sorted_results:
            candidate_name = result.get('candidate_name', 'Unknown Candidate')
            details = result['screened_candidate']
            with st.expander(f"**{candidate_name}** - Score: **{details.score}/100**"):
                st.markdown(f"**📝 Rationale:** {details.rationale}")
                st.markdown("**✅ Strengths:**")
                for strength in details.strengths: st.markdown(f"- {strength}")
                st.markdown("**⚠️ Weaknesses/Gaps:**")
                for weakness in details.weaknesses: st.markdown(f"- {weakness}")
        st.info("You can now proceed to **Phase 3: Interview Prep** to generate questions for these candidates.")

# =================================================================================================
# --- PHASE 3: INTERVIEW PREP ---
# =================================================================================================
with tab3:
    st.header("Generate Tailored Interview Questions")
    if not st.session_state.screening_results:
        st.warning("Please screen candidates in Phase 2 to generate interview questions.")
    else:
        successful_results = [res for res in st.session_state.screening_results if res and res.get('screened_candidate')]
        sorted_results = sorted(successful_results, key=lambda x: x['screened_candidate'].score, reverse=True)
        
        candidate_names = [res.get('candidate_name', 'Unknown') for res in sorted_results]
        
        if not candidate_names:
             st.warning("No candidates were successfully screened.")
        else:
            selected_candidate_name = st.selectbox("Select a candidate to generate interview questions for:", options=candidate_names)
            
            # Find the full result dictionary for the selected candidate
            selected_candidate_result = next((res for res in sorted_results if res.get('candidate_name') == selected_candidate_name), None)

            if selected_candidate_result:
                if st.button(f"Generate Questions for {selected_candidate_name}", type="primary", use_container_width=True):
                    with st.spinner(f"🧠 Generating tailored questions for {selected_candidate_name}..."):
                        details = selected_candidate_result['screened_candidate']
                        try:
                           questions = generate_interview_questions(st.session_state.final_jd, details, selected_candidate_name)
                           st.session_state.interview_questions[selected_candidate_name] = questions
                           st.success(f"Questions generated for {selected_candidate_name}!")
                        except Exception as e:
                            st.error(f"Could not generate questions. Error: {e}")

                # Display the questions if they exist in the session state
                if st.session_state.interview_questions.get(selected_candidate_name):
                    st.subheader(f"Interview Questions for {selected_candidate_name}")
                    questions_data = st.session_state.interview_questions[selected_candidate_name]
                    
                    st.markdown("**Technical Questions:**")
                    for q in questions_data.technical_questions: st.markdown(f"- {q}")
                    
                    st.markdown("**Behavioral Questions:**")
                    for q in questions_data.behavioral_questions: st.markdown(f"- {q}")
                    
                    st.markdown("**Situational Questions (Probing Gaps):**")
                    for q in questions_data.situational_questions: st.markdown(f"- {q}")
