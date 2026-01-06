from fastapi import APIRouter, Query, HTTPException, Path
from typing import Optional

from app.models import Talk, TalksList, TalkQuestion, TalkQuestionResponse
from app.services import talks_service, create_error_response, create_error_response

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


@router.post("/{talk_id}/questions", response_model=TalkQuestionResponse, summary="Submit question for talk", operation_id="submit_talk_question")
async def submit_talk_question(
    talk_id: str = Path(..., description="The ID of the talk to ask about"),
    question: TalkQuestion = ...
):
    """
    Submit a question about a specific talk.
    
    The question will be reviewed and may be featured in future content or Q&A sessions.
    
    - **talk_id**: The unique identifier for the talk
    - **question**: Your question details including name, email, and question text
    """
    result = talks_service.submit_question(talk_id, question.model_dump())
    
    if not result:
        error = create_error_response(
            "not_found",
            f"Talk with ID '{talk_id}' not found",
            {"talk_id": talk_id}
        )
        raise HTTPException(status_code=404, detail=error.model_dump())
    
    return TalkQuestionResponse(**result)