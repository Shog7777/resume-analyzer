import json
import re
import anthropic


def analyze_match(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume vs job description using Claude AI.
    Returns structured match analysis.
    """
    client = anthropic.Anthropic()

    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer.

Analyze the following resume against the job description and return a JSON object with this exact structure:

{{
  "overall_score": <integer 0-100>,
  "skills_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "keywords_score": <integer 0-100>,
  "matched_keywords": [<list of matched keywords/skills, max 15>],
  "missing_keywords": [<list of important missing keywords, max 10>],
  "suggestions": [<list of 3-5 specific improvement suggestions>],
  "summary": "<2-3 sentence analysis summary>"
}}

Scoring criteria:
- overall_score: weighted average of all factors
- skills_score: how well technical and soft skills match
- experience_score: relevance of experience to the role
- keywords_score: percentage of important JD keywords found in resume

Be strict and realistic in scoring — most resumes score 40-80%.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Return ONLY the JSON object, no markdown, no explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    # Clean up response
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)

    result = json.loads(response_text)
    return result
