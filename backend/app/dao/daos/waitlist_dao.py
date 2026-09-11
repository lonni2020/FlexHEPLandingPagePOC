"""Data access for waitlist signups."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.waitlist_signup import WaitlistSignup


class WaitlistDAO(BaseDAO[WaitlistSignup]):
    """CRUD operations for the launch waitlist."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, WaitlistSignup)

    async def get_by_email(self, email: str) -> WaitlistSignup | None:
        """Find a signup by its normalized email address."""
        result = await self.session.execute(
            select(WaitlistSignup).where(WaitlistSignup.email == email)
        )
        return result.scalar_one_or_none()
