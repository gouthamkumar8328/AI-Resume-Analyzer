from openai import OpenAI
import json
import os

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_summary(text):

    prompt = f"""
    Return ONLY valid JSON.

    Analyze the resume thoroughly.

    Rules:
    - ATS Score must be between 0 and 100.
    - Professional Summary must contain 8-12 detailed sentences.
    - Mention education, technical skills, projects, certifications, strengths, and career potential.
    - Do not give a one-line summary.
    - Skills should be comprehensive.
    - Interview questions should be technical and role-specific.

    Return format:

    {{
        "ats_score": 0,
        "professional_summary": "",
        "skills": [],
        "strengths": [],
        "weaknesses": [],
        "projects": [],
        "certifications": [],
        "interview_questions": []
    }}

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ATS resume analyzer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown code blocks if present
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return content