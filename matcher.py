from skills import SKILLS_DB

import re
from skills import SKILLS_DB

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return list(set(found))


def get_match_score(resume_text, job_desc):
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_desc)

    matched = list(set(resume_skills) & set(required_skills))
    missing = list(set(required_skills) - set(resume_skills))

    if len(required_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(required_skills)) * 100
    return round(score, 2), matched, missing, resume_skills, required_skills
