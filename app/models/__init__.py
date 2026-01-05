from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from enum import Enum


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class ProfileMode(str, Enum):
    default = "default"
    conference = "conference"
    afterhours = "afterhours"


class Profile(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Luise Freese",
                "role": "Azure & Power Platform Architect",
                "bio": "Building AI-enabled solutions that work beyond demos",
                "location": "Germany",
                "website": "https://m365princess.com",
                "linkedin": "https://linkedin.com/in/luisefreese",
                "methods": ["Design for longevity, not just demos", "Build accessible apps that everyone can use"],
                "current_focus": "Designing AI-enabled solutions with governance"
            }
        }
    )
    
    name: str
    role: str
    bio: str
    location: str
    website: Optional[str] = None
    linkedin: Optional[str] = None
    methods: List[str]
    current_focus: Optional[str] = None
    favorite_tools: Optional[List[str]] = None


class Quote(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "It depends... but usually the answer is caching.",
                "topic": "general",
                "context": "The universal truth of software development"
            }
        }
    )
    
    text: str
    topic: Optional[str] = None
    context: Optional[str] = None


class Skill(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "azure-architecture",
                "name": "Azure Solutions Architecture",
                "level": "Advanced",
                "domain": "Cloud",
                "tags": ["azure", "cloud-architecture", "integration"],
                "examples": ["Multi-tenant SaaS solutions", "Microservices architecture", "Event-driven systems"]
            }
        }
    )
    
    id: str
    name: str
    level: str
    domain: str
    tags: List[str]
    examples: List[str]


class SkillsList(BaseModel):
    skills: List[Skill]
    total: int


class Talk(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "deploy-on-fridays-bonanni-2026",
                "title": "Let's deploy on Fridays!",
                "description": "Your team sticks to the Friday-freeze-policy? This is super common, but also it gives a certain smell. A smell of low delivery confidence and of low trust in your processes around Testing, QA and rollback. This session won't make you suddenly trust your bubblegum-and-duct-taped delivery pipeline but aims at stripping away the superstition and look at what's really broken when teams are too scared to ship. We'll dig into the real indicators of healthy delivery, like deployment frequency, lead time, change failure rate, recovery time, and why they matter more than any velocity chart ever will.",
                "year": 2026,
                "venue": "Bonanni a tutti, Turin",
                "topics": ["DevOps", "Deployment", "CI/CD", "Testing", "QA", "Delivery Metrics", "Team Culture"],
                "slides_url": None
            }
        }
    )
    
    id: str
    title: str
    description: str
    year: int
    venue: Optional[str] = None
    topics: List[str]
    slides_url: Optional[str] = None


class TalksList(BaseModel):
    talks: List[Talk]
    total: int


class TalkQuestion(BaseModel):
    name: str
    question: str


class TalkQuestionResponse(BaseModel):
    id: str
    message: str
    talk_id: str


class Project(BaseModel):
    id: str
    name: str
    description: str
    status: str
    tech_stack: List[str]
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    highlights: List[str]


class ProjectsList(BaseModel):
    projects: List[Project]
    total: int


