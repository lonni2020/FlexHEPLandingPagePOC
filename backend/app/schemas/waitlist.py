"""Request and response schemas for the launch waitlist."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class WaitlistSignupRequest(BaseModel):
    """Payload submitted by the landing page."""

    email: EmailStr = Field(description="Email address for FlexHEP launch updates")


class WaitlistSignupResponse(BaseModel):
    """Successful waitlist response."""

    message: str
    created_at: datetime
