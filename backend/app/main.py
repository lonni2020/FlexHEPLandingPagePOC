"""
FastAPI Application Entry Point

This module creates and configures the FastAPI application.
Routes are organized into routers and included with prefixes.

ROUTER ORGANIZATION:
    /health          - Health check
    /api/v1/waitlist - Launch waitlist signup
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.waitlist import router as waitlist_router
from app.core.config import settings
from app.database.connection import init_db

logger = settings.logger
logger.info(
    f"Starting {settings.app_name} in {settings.environment} environment "
    f"with log level: {settings.log_level}"
)

# =============================================================================
# CONFIGURATION - Modify these values for your project
# =============================================================================
API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/", response_model=None)
async def root() -> dict | FileResponse:
    """Serve the landing page when built, otherwise expose API metadata."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": settings.app_name, "version": settings.app_version}


# Include routers with API prefix
app.include_router(waitlist_router, prefix=f"{API_PREFIX}/waitlist")

static_dir = Path(__file__).resolve().parents[2] / "frontend" / "dist"
try:
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
except RuntimeError:
    logger.info("Frontend build not found; serving API only")
