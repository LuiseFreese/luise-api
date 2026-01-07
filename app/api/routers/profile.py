from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional, List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models import Profile, Quote
from app.services import profile_service, create_error_response

# Rate limiter instance  
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=Profile, summary="Get profile information", operation_id="get_profile")
@limiter.limit("60/minute")  # Allow 60 requests per minute
async def get_profile(request: Request):
    """
    Get the main profile information.
    
    **Rate limit:** 60 requests per minute per IP address
    """
    return profile_service.get_profile()


@router.get("/quotes", response_model=Quote, summary="Get a quote", operation_id="get_quote")  
@limiter.limit("30/minute")  # Allow 30 quote requests per minute
async def get_quote(
    request: Request,
    topic: Optional[str] = Query(None, description="Quote topic (e.g., general, ai)")
):
    """
    Get a programming-related quote, optionally filtered by topic.
    
    Available topics: general, ai
    """
    return profile_service.get_quote(topic=topic)