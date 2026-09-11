"""
Database Connection and Session Management

This module configures the async SQLAlchemy engine and session factory for SQLite.

KEY CONCEPTS:
- Engine: The connection pool manager (one per application)
- Session: A single database conversation (one per request)
- Base: The declarative base class all models inherit from

USAGE:
    from app.database.connection import get_session, Base

    # In FastAPI routes (via dependency injection):
    @router.get("/items")
    async def get_items(session: AsyncSession = Depends(get_session)):
        ...

    # For creating tables:
    await init_db()
"""

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

logger = settings.logger

# SQLite does not create parent directories for a file-backed database.
Path("data").mkdir(parents=True, exist_ok=True)


def create_engine() -> AsyncEngine:
    """
    Create the async SQLite engine.

    Returns:
        AsyncEngine: Configured SQLAlchemy async engine
    """
    logger.info("Initializing async SQLite database connection")

    return create_async_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )


# Create the engine singleton
engine = create_engine()
logger.info("Async SQLite engine created")

# Session factory - creates new sessions for each request
session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,  # Explicit transaction control
    autoflush=False,  # Manual flush control (flush before queries)
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    All database models should inherit from this class:

        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(primary_key=True)
            ...
    """

    pass


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Dependency for FastAPI to inject database sessions.

    This is the primary way to get database access in routes:

        @router.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Item))
            return result.scalars().all()

    The session is automatically closed when the request completes.

    Yields:
        AsyncSession: Database session for the current request
    """
    async with session_factory() as session:
        yield session


async def init_db() -> None:
    """
    Initialize database by creating all tables.

    This uses SQLAlchemy's create_all() which is idempotent -
    it only creates tables that don't exist.

    For production, use Alembic migrations instead.
    """
    # Import models to register them with Base.metadata
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
