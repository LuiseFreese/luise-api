from fastapi import APIRouter, Query
from typing import Optional

from app.models import Talk, TalksList
from app.services import talks_service, create_error_response

router = APIRouter(prefix="/talks", tags=["Talks"])


@router.get("", response_model=TalksList, summary="Get all talks", operation_id="list_talks")
async def get_talks(
    year: Optional[int] = Query(None, description="Filter talks by year")
):
    """
    Get a list of talks, optionally filtered by year.
    
    - **year**: Filter talks by the year they were given
    """
    talks = talks_service.get_talks(year=year)
    return TalksList(talks=talks, total=len(talks))