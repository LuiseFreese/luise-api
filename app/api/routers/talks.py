from fastapi import APIRouter, Query, HTTPException, Path
from typing import Optional, List

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
    - **question**: Your question details including name, contact email, and question text
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


@router.get("/{talk_id}/questions", summary="Get questions for talk (debug)", operation_id="get_talk_questions")
async def get_talk_questions(
    talk_id: str = Path(..., description="The ID of the talk to get questions for")
):
    """
    Debug endpoint to view submitted questions for a talk.
    """
    import json
    import os
    from pathlib import Path
    
    # Get questions file path
    questions_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "questions.json")
    questions_file = os.path.abspath(questions_file)
    
    debug_info = {
        "questions_file_path": questions_file,
        "file_exists": os.path.exists(questions_file),
        "questions": []
    }
    
    if os.path.exists(questions_file):
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                all_questions = json.load(f)
                
            # Filter questions for this talk
            talk_questions = [q for q in all_questions if q.get('talk_id') == talk_id]
            debug_info["questions"] = talk_questions
            debug_info["total_questions"] = len(all_questions)
            debug_info["talk_questions"] = len(talk_questions)
            
        except Exception as e:
            debug_info["error"] = str(e)
    
    return debug_info