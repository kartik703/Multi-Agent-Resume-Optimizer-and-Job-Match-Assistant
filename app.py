# app.py

import streamlit as st
import os
from dotenv import load_dotenv
from agents.resume_analyzer import ResumeAnalyzer
from agents.jd_reader import JDReader
from agents.gap_finder import GapFinder
from agents.resume_rewriter import ResumeRewriter

load_dotenv()

# Streamlit Page Setup
st.set_page_config(page_title="🛠️ Resume Optimizer Pro", layout="wide")
st.title("📄 Multi-Agent Resume Optimizer and Job Match Assistant (PRO)")
st.caption("Analyze Resume 📄 | Match JD 📝 | Improve Resume ✨ (Powered by OpenAI GPT-4)")

# Initialize Agents
resume_analyzer = ResumeAnalyzer()
jd_reader = JDReader()
gap_finder = GapFinder()
resume_rewriter = ResumeRewriter()

# Step 1: Upload Resume
st.header("Step 1: Upload Your Resume")
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Step 2: Paste Job Description
st.header("Step 2: Paste the Job Description")
jd_text = st.text_area("Paste the complete Job Description here:", height=300)

# Step 3: Analyze Button
if st.button("Analyze Resume vs Job Description"):
    if resume_file is not None and jd_text.strip() != "":
        # Save uploaded resume to temporary file
        temp_resume_path = resume_file.name
        with open(temp_resume_path, "wb") as f:
            f.write(resume_file.getbuffer())

        # Analyze Resume
        with st.spinner("🔎 Analyzing Resume..."):
            resume_result = resume_analyzer.analyze_resume(temp_resume_path)

        # Analyze Job Description
        with st.spinner("🔎 Analyzing Job Description..."):
            jd_result = jd_reader.extract_info_from_jd(jd_text)

        # Find Gaps
        with st.spinner("🔎 Finding Skill Gaps..."):
            gap_result = gap_finder.find_skill_gaps(resume_result["extracted_info"], jd_result)

        # Suggest Resume Improvements
        with st.spinner("🔎 Suggesting Resume Improvements..."):
            all_missing_skills = []
            for category in gap_result["detailed_gap"].values():
                all_missing_skills.extend(category["missing"])
            rewrite_suggestions = resume_rewriter.suggest_resume_improvements(all_missing_skills, jd_result.get("role_title", "Unknown Role"))

        # Display Results
        st.success(f"✅ Overall Resume to JD Match: {gap_result['match_percentage']}%")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 Extracted Resume Information:")
            st.json(resume_result["extracted_info"])

        with col2:
            st.subheader("📋 Extracted Job Description Information:")
            st.json(jd_result)

        st.header("🔍 Detailed Skill Gap Analysis:")

        for category, values in gap_result["detailed_gap"].items():
            st.subheader(f"Category: {category.replace('_', ' ').title()}")
            st.write(f"✅ Skills Matched: {', '.join(values['matched']) if values['matched'] else 'None'}")
            st.write(f"❌ Skills Missing: {', '.join(values['missing']) if values['missing'] else 'None'}")

        st.header("🛠 Resume Improvement Suggestions:")
        st.markdown(rewrite_suggestions)

        # Clean up temporary resume file
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)

    else:
        st.error("⚠️ Please upload a Resume and paste a Job Description before analyzing!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Kartik703 | Powered by OpenAI | 2025")
