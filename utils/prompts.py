# utils/prompts.py

def get_resume_prompt(resume_text):
    return f"""
You are an expert resume analyzer. Carefully read the resume text below and extract:
- Programming Languages
- Technical Skills
- Soft Skills
- Tools & Technologies
- Certifications

Provide your output in JSON format like this:
{{
"programming_languages": [],
"technical_skills": [],
"soft_skills": [],
"tools_technologies": [],
"certifications": []
}}

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""

def get_jd_prompt(jd_text):
    return f"""
You are an expert job description analyzer. Carefully read the job description below and extract:
- Required Programming Languages
- Required Technical Skills
- Required Soft Skills
- Required Tools & Technologies
- Required Certifications
- Expected Role Title

Provide your output in JSON format like this:
{{
"programming_languages": [],
"technical_skills": [],
"soft_skills": [],
"tools_technologies": [],
"certifications": [],
"role_title": ""
}}

Job Description Text:
\"\"\"
{jd_text}
\"\"\"
"""

def get_resume_rewrite_prompt(missing_skills, role_title):
    return f"""
You are an expert career advisor helping candidates improve their resumes.

The candidate is applying for the role of "{role_title}".  
They are missing the following skills in their resume: {', '.join(missing_skills)}.

For each missing skill, suggest 1–2 short bullet points they can add to their resume (even if they don't have direct experience, recommend transferable skills or learning projects).

Respond ONLY with improvement suggestions, organized by skill.

Example Format:
- **Skill Name**:
  - Suggestion 1
  - Suggestion 2
"""
