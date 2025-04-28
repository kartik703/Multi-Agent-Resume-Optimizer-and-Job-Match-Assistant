# agents/resume_rewriter.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.prompts import get_resume_prompt
from utils.file_reader import extract_text_from_pdf, extract_text_from_docx

load_dotenv()

class ResumeRewriter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def suggest_resume_improvements(self, missing_skills, role_title):
        if not missing_skills:
            return "✅ Your resume already covers all the required skills for this role. Great job!"

        prompt = f"""
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

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        suggestions = response.choices[0].message.content
        return suggestions
