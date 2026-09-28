from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Resume Parser and Screening System")

class ScreeningRequest(BaseModel):
    resume_text: str
    job_description: str

class ScreeningResult(BaseModel):
    skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    score: float

SKILLS = {"python", "java", "c#", "sql", "docker", "kubernetes", "aws", "azure", "react", "typescript", "machine learning", "pytorch", "tensorflow", "fastapi", "git"}

def extract_skills(text: str) -> list[str]:
    normalized = text.lower()
    return sorted(skill for skill in SKILLS if re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", normalized))

def screen(resume_text: str, job_description: str) -> ScreeningResult:
    resume_skills = set(extract_skills(resume_text))
    required = set(extract_skills(job_description))
    matched = sorted(resume_skills & required)
    missing = sorted(required - resume_skills)
    score = round((len(matched) / len(required)) * 100, 2) if required else 0.0
    return ScreeningResult(skills=sorted(resume_skills), matched_skills=matched, missing_skills=missing, score=score)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/screen", response_model=ScreeningResult)
def screen_resume(request: ScreeningRequest) -> ScreeningResult:
    return screen(request.resume_text, request.job_description)
