import json
import time
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from collections import defaultdict, deque

from app.models import (
    Profile, Quote, Skill, Talk, Project, 
    ErrorDetail, ErrorResponse
)


class DataService:
    """Service for loading and managing static data."""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self._profile_data = None
        self._skills_data = None
        self._talks_data = None
        self._projects_data = None
        self._quotes_data = None
        
    def _load_json(self, filename: str) -> Any:
        """Load JSON data from file."""
        with open(self.data_dir / filename, 'r') as f:
            return json.load(f)
    
    @property
    def profile_data(self) -> Dict[str, Any]:
        if self._profile_data is None:
            self._profile_data = self._load_json("profile.json")
        return self._profile_data
    
    @property
    def skills_data(self) -> List[Dict[str, Any]]:
        if self._skills_data is None:
            self._skills_data = self._load_json("skills.json")
        return self._skills_data
    
    @property
    def talks_data(self) -> List[Dict[str, Any]]:
        if self._talks_data is None:
            self._talks_data = self._load_json("talks.json")
        return self._talks_data
    
    @property
    def projects_data(self) -> List[Dict[str, Any]]:
        if self._projects_data is None:
            self._projects_data = self._load_json("projects.json")
        return self._projects_data
    
    @property
    def quotes_data(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._quotes_data is None:
            self._quotes_data = self._load_json("quotes.json")
        return self._quotes_data


class RateLimitService:
    """Simple in-memory rate limiting service."""
    
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_rate_limited(self, key: str) -> bool:
        """Check if a key is rate limited."""
        now = time.time()
        request_times = self.requests[key]
        
        # Remove old requests outside the time window
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        # Check if we're at the limit
        if len(request_times) >= self.max_requests:
            return True
        
        # Add current request
        request_times.append(now)
        return False
    
    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests for a key."""
        now = time.time()
        request_times = self.requests[key]
        
        # Remove old requests
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        return max(0, self.max_requests - len(request_times))


class ProfileService:
    """Service for profile-related operations."""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    def get_profile(self) -> Profile:
        """Get basic profile information."""
        data = self.data_service.profile_data
        
        # Base profile data
        profile_data = {
            "name": data["name"],
            "role": data["role"],
            "bio": data["bio"],
            "location": data["location"],
            "website": data.get("website"),
            "linkedin": data.get("linkedin"),
            "methods": data["methods"]
        }
        
        # Add default mode data
        mode_data = data["modes"]["default"]
        profile_data.update(mode_data)
        
        return Profile(**profile_data)

    def get_quote(self, topic: Optional[str] = None) -> Quote:
        """Get a quote, optionally filtered by topic."""
        quotes_data = self.data_service.quotes_data
        
        if topic and topic in quotes_data:
            quotes_list = quotes_data[topic]
        else:
            # Default to general quotes if topic not found
            quotes_list = quotes_data.get("general", [])
        
        # For demo, just return the first quote
        if quotes_list:
            quote_data = quotes_list[0]
            return Quote(**quote_data)
        
        # Fallback quote
        return Quote(
            text="It depends... but documentation usually helps.",
            topic=topic or "general",
            context="When in doubt, always a safe answer"
        )


class SkillsService:
    """Service for skills-related operations."""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    def get_skills(self, domain: Optional[str] = None) -> List[Skill]:
        """Get skills, optionally filtered by domain."""
        skills_data = self.data_service.skills_data
        
        if domain:
            filtered_skills = [s for s in skills_data if s["domain"].lower() == domain.lower()]
        else:
            filtered_skills = skills_data
        
        return [Skill(**skill) for skill in filtered_skills]


class TalksService:
    """Service for talks-related operations."""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    def get_talks(self, year: Optional[int] = None) -> List[Talk]:
        """Get talks, optionally filtered by year."""
        talks_data = self.data_service.talks_data
        
        if year:
            filtered_talks = [t for t in talks_data if t["year"] == year]
        else:
            filtered_talks = talks_data
        
        return [Talk(**talk) for talk in filtered_talks]
    
    def submit_question(self, talk_id: str, question_data: dict) -> dict:
        """Submit a question for a specific talk."""
        import uuid
        import json
        import os
        from datetime import datetime
        
        # Verify talk exists
        talks_data = self.data_service.talks_data
        talk_exists = any(talk["id"] == talk_id for talk in talks_data)
        
        if not talk_exists:
            return None
            
        # Generate question ID and timestamp
        question_id = f"q_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow().isoformat()
        
        # Create question record
        question_record = {
            "id": question_id,
            "talk_id": talk_id,
            "name": question_data["name"],
            "email": question_data["email"], 
            "question": question_data["question"],
            "submitted_at": timestamp,
            "status": "received"
        }
        
        # Save to questions.json file
        questions_file = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")
        questions_file = os.path.abspath(questions_file)
        
        print(f"Attempting to save question to: {questions_file}")
        print(f"Directory exists: {os.path.exists(os.path.dirname(questions_file))}")
        print(f"File exists: {os.path.exists(questions_file)}")
        print(f"Directory is writable: {os.access(os.path.dirname(questions_file), os.W_OK) if os.path.exists(os.path.dirname(questions_file)) else 'N/A'}")
        
        try:
            # Load existing questions or create empty list
            if os.path.exists(questions_file):
                with open(questions_file, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
                    print(f"Loaded {len(questions)} existing questions")
            else:
                questions = []
                print("Creating new questions list")
            
            # Add new question
            questions.append(question_record)
            print(f"Added question {question_id}, total questions: {len(questions)}")
            
            # Save back to file
            os.makedirs(os.path.dirname(questions_file), exist_ok=True)
            with open(questions_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            
            print(f"Question saved successfully to {questions_file}")
            
        except Exception as e:
            print(f"Error saving question: {e}")
            # Continue anyway, don't fail the API call
        
        print(f"Question saved to {questions_file}: {question_id}")
        
        return {
            "id": question_id,
            "message": "Thanks for your question, I'll answer this soon!",
            "talk_id": talk_id,
            "status": "received"
        }
    



class ProjectsService:
    """Service for projects-related operations."""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    def get_projects(self) -> List[Project]:
        """Get all projects."""
        projects_data = self.data_service.projects_data
        return [Project(**project) for project in projects_data]


def create_error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> ErrorResponse:
    """Helper function to create consistent error responses."""
    return ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            details=details
        )
    )


# Global service instances
data_service = DataService()
rate_limit_service = RateLimitService()
profile_service = ProfileService(data_service)
skills_service = SkillsService(data_service)
talks_service = TalksService(data_service)
projects_service = ProjectsService(data_service)