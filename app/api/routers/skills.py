from fastapi import APIRouter, Query
from typing import Optional

from app.models import Skill, SkillsList
from app.services import skills_service, create_error_response

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("", response_model=SkillsList, summary="Get all skills", operation_id="list_skills")
async def get_skills(
    domain: Optional[str] = Query(None, description="Filter by skill domain (e.g., Cloud, Low-Code, Security, DevOps)")
):
    """
    Get a list of skills, optionally filtered by domain.
    
    Available domains: Cloud, Low-Code, Collaboration, AI, Security, DevOps, Quality, Architecture, Development, Strategy
    """
    skills = skills_service.get_skills(domain=domain)
    return SkillsList(skills=skills, total=len(skills))