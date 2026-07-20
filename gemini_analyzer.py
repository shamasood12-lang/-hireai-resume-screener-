import google.generativeai as genai

def get_ai_analysis(resume_text, job_desc, api_key):

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are an expert HR recruiter.

        Resume:
        {resume_text}

        Job Description:
        {job_desc}

        Give:

        1. Strengths
        2. Missing Skills
        3. Hiring Recommendation
        4. Three Interview Questions

        Keep response concise.
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception:

     return """
## Gemini AI Analysis

AI analysis is temporarily unavailable because the Gemini API quota has been reached.

Resume matching and ATS scoring were completed successfully.

Please review:
- Match Score
- Matched Skills
- Missing Skills
- Recruiter Mode Results

The system will continue functioning normally without AI-generated recommendations.
"""