from fastapi import FastAPI
from pydantic import BaseModel
import re
import spacy
from spacy.matcher import PhraseMatcher

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
nlp = spacy.blank("en")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("SKILL", [nlp.make_doc(skill) for skill in SKILLS])

def extract_skills(text: str) -> list[str]:
    document = nlp(text)
    matched = {document[start:end].text.lower() for _, start, end in matcher(document)}
    return sorted(skill for skill in SKILLS if skill in matched or re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", text.lower()))

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
