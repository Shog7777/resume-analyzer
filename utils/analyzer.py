import json
import re
import os
import urllib.request
import urllib.error


def analyze_match(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume vs job description using Google Gemini API.
    Returns structured match analysis.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")

    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer.

Analyze the resume against the job description and return ONLY a JSON object with this exact structure, no markdown, no explanation:

{{
  "overall_score": <integer 0-100>,
  "skills_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "keywords_score": <integer 0-100>,
  "matched_keywords": ["keyword1", "keyword2"],
  "missing_keywords": ["keyword1", "keyword2"],
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "summary": "2-3 sentence analysis summary"
}}

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:1500]}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1500}
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))

    response_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)

    return json.loads(response_text)
