import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_profile_endpoint():
    """Test profile endpoint returns correct structure and data."""
    response = client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "name" in data
    assert "role" in data
    assert "bio" in data
    assert "location" in data
    assert "methods" in data
    assert "website" in data
    assert "linkedin" in data
    
    # Check data values
    assert data["name"] == "Luise Freese"
    assert data["website"] == "https://m365princess.com"
    assert data["linkedin"] == "https://linkedin.com/in/luisefreese"
    assert isinstance(data["methods"], list)
    assert len(data["methods"]) > 0


def test_skills_get_all():
    """Test getting all skills."""
    response = client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    
    assert "skills" in data
    assert "total" in data
    assert isinstance(data["skills"], list)
    assert data["total"] == len(data["skills"])
    
    # Check skill structure if any exist
    if len(data["skills"]) > 0:
        skill = data["skills"][0]
        assert "id" in skill
        assert "name" in skill
        assert "domain" in skill
        assert "level" in skill


def test_skills_filter_by_domain():
    """Test filtering skills by domain."""
    response = client.get("/skills?domain=AI")
    assert response.status_code == 200
    data = response.json()
    
    assert "skills" in data
    assert "total" in data
    
    # All returned skills should be in AI domain
    for skill in data["skills"]:
        assert skill["domain"] == "AI"


def test_skills_filter_nonexistent_domain():
    """Test filtering skills by non-existent domain returns empty list."""
    response = client.get("/skills?domain=NonExistent")
    assert response.status_code == 200
    data = response.json()
    
    assert "skills" in data
    assert "total" in data
    assert len(data["skills"]) == 0
    assert data["total"] == 0


def test_talks_get_all():
    """Test getting all talks."""
    response = client.get("/talks")
    assert response.status_code == 200
    data = response.json()
    
    assert "talks" in data
    assert "total" in data
    assert isinstance(data["talks"], list)
    assert data["total"] == len(data["talks"])
    
    # Check talk structure if any exist
    if len(data["talks"]) > 0:
        talk = data["talks"][0]
        assert "id" in talk
        assert "title" in talk
        assert "description" in talk
        assert "year" in talk


def test_talks_filter_by_year():
    """Test filtering talks by year."""
    response = client.get("/talks?year=2025")
    assert response.status_code == 200
    data = response.json()
    
    assert "talks" in data
    assert "total" in data
    
    # All returned talks should be from 2025
    for talk in data["talks"]:
        assert talk["year"] == 2025


def test_talks_filter_nonexistent_year():
    """Test filtering talks by non-existent year returns empty list."""
    response = client.get("/talks?year=1999")
    assert response.status_code == 200
    data = response.json()
    
    assert "talks" in data
    assert "total" in data
    assert len(data["talks"]) == 0
    assert data["total"] == 0


def test_submit_talk_question():
    """Test submitting a question for an existing talk."""
    # First get all talks to find a valid talk ID
    talks_response = client.get("/talks")
    talks_data = talks_response.json()
    assert len(talks_data["talks"]) > 0
    
    talk_id = talks_data["talks"][0]["id"]
    
    question_data = {
        "name": "Test User",
        "email": "test@example.com",
        "question": "This is a test question about your talk. How do you handle edge cases?"
    }
    
    response = client.post(f"/talks/{talk_id}/questions", json=question_data)
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert "message" in data
    assert "talk_id" in data
    assert "status" in data
    assert data["talk_id"] == talk_id
    assert data["status"] == "received"


def test_submit_question_invalid_talk():
    """Test submitting a question for a non-existent talk returns 404."""
    question_data = {
        "name": "Test User", 
        "email": "test@example.com",
        "question": "This is a test question."
    }
    
    response = client.post("/talks/nonexistent-talk/questions", json=question_data)
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_submit_question_validation():
    """Test question validation requirements."""
    # Test missing required fields
    response = client.post("/talks/any-talk/questions", json={})
    assert response.status_code == 422
    
    # Test short question (less than 10 characters)
    short_question = {
        "name": "Test User",
        "email": "test@example.com", 
        "question": "Too short"
    }
    response = client.post("/talks/any-talk/questions", json=short_question)
    assert response.status_code == 422


def test_projects_get_all():
    """Test getting all projects."""
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    
    assert "projects" in data
    assert "total" in data
    assert isinstance(data["projects"], list)
    assert data["total"] == len(data["projects"])
    
    # Check project structure if any exist
    if len(data["projects"]) > 0:
        project = data["projects"][0]
        assert "id" in project
        assert "name" in project
        assert "description" in project
        assert "status" in project
        assert "tech_stack" in project


def test_health_check():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint_serves_docs():
    """Test the root endpoint serves swagger docs."""
    response = client.get("/")
    assert response.status_code == 200
    # Root now serves the swagger UI directly
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()