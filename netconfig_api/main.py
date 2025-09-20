"""Main FastAPI application for NetConfigAPI."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from netconfig_api.api.hostname import router as hostname_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger.info("Starting NetConfigAPI application")
    yield
    logger.info("Shutting down NetConfigAPI application")


app = FastAPI(
    title="NetConfigAPI",
    description="A vendor-agnostic API that translates a standard REST interface into network configuration commands",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    hostname_router,
    prefix="/api/v1",
    tags=["hostname"]
)


@app.get("/")
async def root() -> dict:
    """Root endpoint providing API information."""
    return {
        "name": "NetConfigAPI",
        "version": "0.1.0",
        "description": "A vendor-agnostic API for network device configuration",
        "docs_url": "/docs",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "NetConfigAPI"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
