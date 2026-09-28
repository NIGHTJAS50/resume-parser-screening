from app.main import extract_skills, screen

def test_extract_skills_is_case_insensitive():
    assert extract_skills("Built APIs with Python, FastAPI and Docker") == ["docker", "fastapi", "python"]

def test_screening_returns_match_score_and_gap():
    result = screen("Python Docker", "Python Docker Kubernetes")
    assert result.matched_skills == ["docker", "python"]
    assert result.missing_skills == ["kubernetes"]
    assert result.score == 66.67
