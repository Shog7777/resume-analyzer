import json
import re
import os
import requests


def analyze_match(resume_text: str, job_description: str) -> dict:
    api_key = os.environ.get("GROQ_API_KEY", "")

    prompt = f"""You are an expert ATS analyzer. Analyze the resume against the job description.
Return ONLY a JSON object, no markdown, no explanation:

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

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "resume-analyzer/1.0"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.1
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")

    response_text = response.json()["choices"][0]["message"]["content"].strip()
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)

    return json.loads(response_text)
