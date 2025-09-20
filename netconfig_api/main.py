"""NetConfig API - Main FastAPI application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from netconfig_api.api.endpoints import hostname


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    print("NetConfig API starting up...")
    yield
    # Shutdown
    print("NetConfig API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="NetConfig API",
    description="A vendor-agnostic API that translates a standard REST interface into "
    "network configuration commands",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    hostname.router,
    tags=["Hostname Configuration"],
    responses={404: {"description": "Not found"}},
)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Root endpoint - API health check."""
    return {"message": "NetConfig API is running", "version": "0.1.0", "status": "healthy"}


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "netconfig-api", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("netconfig_api.main:app", host="0.0.0.0", port=8000, reload=True)
