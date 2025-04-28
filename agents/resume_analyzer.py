# agents/resume_analyzer.py

import pdfplumber
import docx
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.prompts import get_resume_prompt
from utils.file_reader import extract_text_from_pdf, extract_text_from_docx

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_text_from_pdf(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def analyze_resume(self, file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format! Only PDF and DOCX supported.")
        
        extracted_info = self.extract_skills_with_llm(text)
        
        return {
            "raw_text": text,
            "extracted_info": extracted_info
        }

    def extract_skills_with_llm(self, resume_text):
        prompt = f"""
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
            print("Error parsing JSON from LLM:", e)
            return {}
