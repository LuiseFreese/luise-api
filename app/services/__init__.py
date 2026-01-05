import json
import time
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