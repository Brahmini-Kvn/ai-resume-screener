# app/services/evaluator.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def evaluate_resume(resume_text: str, job_description: str):
    prompt = f"""
You are an expert technical recruiter. Given the following job description and resume text, do 3 things:

1. Score the resume from 1 to 10 for how well it matches the job description.
2. Provide a short summary of the resume's strengths and weaknesses.
3. State clearly whether the resume is a strong fit, partial fit, or poor fit.

Respond in this format:
Score: <score>/10
Summary: <summary>
Fit: <Strong Fit | Partial Fit | Poor Fit>

---

Job Description:
\"\"\"
{job_description}
\"\"\"

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
