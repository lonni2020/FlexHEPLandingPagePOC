"""Business logic for the FlexHEP launch waitlist."""

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.config import settings
from app.dao.factory import DAOFactory
from app.schemas.waitlist import WaitlistSignupResponse

logger = settings.logger


class WaitlistService:
    """Coordinate waitlist validation and persistence."""

    def __init__(self, dao_factory: DAOFactory = Depends(DAOFactory)):
        self.waitlist_dao = dao_factory.get_waitlist_dao()

    async def signup(self, email: str) -> WaitlistSignupResponse:
        """Store an email once and return a user-safe response."""
        normalized_email = email.strip().lower()

        try:
            if await self.waitlist_dao.get_by_email(normalized_email):
                raise HTTPException(
                    status_code=409,
                    detail="That email is already on the FlexHEP list.",
                )

            signup = await self.waitlist_dao.create(email=normalized_email)
            return WaitlistSignupResponse(
                message="You are on the FlexHEP list.",
                created_at=signup.created_at,
            )
        except HTTPException:
            raise
        except IntegrityError:
            logger.info("Duplicate waitlist signup rejected")
            raise HTTPException(
                status_code=409,
                detail="That email is already on the FlexHEP list.",
            ) from None
        except SQLAlchemyError as error:
            logger.error("Waitlist database error: %s", error, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="We could not save your email. Please try again.",
            ) from error
