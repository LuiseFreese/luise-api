from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List

from app.models import Profile, Quote
from app.services import profile_service, create_error_response

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=Profile, summary="Get profile information", operation_id="get_profile")
async def get_profile():
    """
    Get the main profile information.
    """
    return profile_service.get_profile()


@router.get("/quotes", response_model=Quote, summary="Get a quote", operation_id="get_quote")
async def get_quote(
    topic: Optional[str] = Query(None, description="Quote topic (e.g., general, ai)")
):
    """
    Get a programming-related quote, optionally filtered by topic.
    
    Available topics: general, ai
    """
    return profile_service.get_quote(topic=topic)