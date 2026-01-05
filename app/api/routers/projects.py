from fastapi import APIRouter
from typing import List

from app.models import Project, ProjectsList
from app.services import projects_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=ProjectsList, summary="Get all projects", operation_id="list_projects")
async def get_projects():
    """
    Get a list of all projects.
    
    Returns information about current and past projects including status,
    tech stack, and links to demos or repositories.
    """
    projects = projects_service.get_projects()
    return ProjectsList(projects=projects, total=len(projects))