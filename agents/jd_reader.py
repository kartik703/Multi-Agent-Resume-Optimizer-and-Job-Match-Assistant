# agents/jd_reader.py
from utils.prompts import get_resume_prompt
from utils.file_reader import extract_text_from_pdf, extract_text_from_docx

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class JDReader:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_info_from_jd(self, jd_text):
        prompt = f"""
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

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        output = response.choices[0].message.content
        
        try:
            import json
            extracted_info = json.loads(output)
            return extracted_info
        except Exception as e:
            print("Error parsing JD JSON:", e)
            return {}
