# agents/gap_finder.py
from utils.prompts import get_resume_prompt
from utils.file_reader import extract_text_from_pdf, extract_text_from_docx

class GapFinder:
    def __init__(self):
        pass

    def find_skill_gaps(self, resume_info, jd_info):
        # Lowercase everything for comparison
        def lower_list(l):
            return [item.lower() for item in l]

        categories = ["programming_languages", "technical_skills", "soft_skills", "tools_technologies", "certifications"]
        
        detailed_gap = {}
        total_skills = 0
        total_matched = 0

        for category in categories:
            resume_skills = lower_list(resume_info.get(category, []))
            jd_skills = lower_list(jd_info.get(category, []))
            
            matched = [skill for skill in jd_skills if skill in resume_skills]
            missing = [skill for skill in jd_skills if skill not in resume_skills]

            detailed_gap[category] = {
                "matched": matched,
                "missing": missing,
                "jd_total": len(jd_skills),
                "matched_count": len(matched)
            }

            total_skills += len(jd_skills)
            total_matched += len(matched)

        # Calculate Overall Match Percentage
        match_percentage = round((total_matched / total_skills) * 100, 2) if total_skills else 0

        return {
            "detailed_gap": detailed_gap,
            "match_percentage": match_percentage
        }
