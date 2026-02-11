import streamlit as st

# Use wide layout for better visualization - Must be the first Streamlit command
st.set_page_config(page_title="Resume Ranking System", layout="wide")

import pandas as pd
from utils import extract_text_from_pdf, extract_text_from_docx, calculate_scores
import db_utils

def main():
    st.title("📄 AI Resume Ranking System")
    st.success("App loaded successfully!") # Debug message
    st.markdown("Upload resumes and a job description to rank candidates based on relevance.")

    # Sidebar for DB Status
    with st.sidebar:
        st.header("Database Config")
        if st.button("Initialize Database"):
            success, msg = db_utils.init_db()
            if success:
                st.success(msg)
            else:
                st.error(msg)
        
        st.markdown("---")
        st.info("Ensure MySQL is running on localhost with root user (no password).")

    # Main Inputs
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1️⃣ Job Description")
        job_description = st.text_area("Paste the Job Description here", height=300)

    with col2:
        st.subheader("2️⃣ Upload Resumes")
        uploaded_files = st.file_uploader("Upload PDF or DOCX files", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Rank Resumes", type="primary"):
        if not job_description:
            st.warning("⚠️ Please enter a Job Description.")
        elif not uploaded_files:
            st.warning("⚠️ Please upload at least one resume.")
        else:
            with st.spinner("Processing resumes..."):
                try:
                    # 1. Parse Resumes
                    resumes_data = []
                    for uploaded_file in uploaded_files:
                        if uploaded_file.name.endswith(".pdf"):
                            text = extract_text_from_pdf(uploaded_file)
                        elif uploaded_file.name.endswith(".docx"):
                            text = extract_text_from_docx(uploaded_file)
                        else:
                            continue
                        
                        resumes_data.append({'name': uploaded_file.name, 'text': text})

                    # 2. Calculate Scores
                    if resumes_data:
                        scores_df = calculate_scores(resumes_data, job_description)
                        
                        st.subheader("3️⃣ Ranking Results")
                        # Display top candidates with highlight
                        st.dataframe(scores_df.style.highlight_max(axis=0))
                        
                        # Bar chart for visual comparison
                        st.bar_chart(data=scores_df, x="Resume", y="Score")

                        # 3. Save to DB
                        try:
                            # Verify DB exists first by trying to save
                            # We'll rely on the user having clicked Init DB or it existing.
                            # But let's wrap in a try-catch for UX.
                            job_id = db_utils.save_job(job_description)
                            db_utils.save_results(job_id, scores_df)
                            st.toast("✅ Results saved to Database!", icon="💾")
                        except Exception as e:
                            st.error(f"Could not save to database. Did you initialize it? Error: {e}")
                    else:
                        st.error("Could not extract text from uploaded files.")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
