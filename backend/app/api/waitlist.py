"""Waitlist API routes."""

from fastapi import APIRouter, Depends, status

from app.schemas.waitlist import WaitlistSignupRequest, WaitlistSignupResponse
from app.service.waitlist_service import WaitlistService

router = APIRouter(tags=["waitlist"])


@router.post(
    "",
    response_model=WaitlistSignupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_waitlist_signup(
    request: WaitlistSignupRequest,
    service: WaitlistService = Depends(WaitlistService),
) -> WaitlistSignupResponse:
    """Add an email to the FlexHEP launch waitlist."""
    return await service.signup(str(request.email))
