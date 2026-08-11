import os
import sys

# Add current backend folder to python path for modular imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from core.middleware import setup_middleware
from core.settings import settings
from api.v1.routes import admin, evaluation, health, ingest, search, session

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
)

# Setup CORS and application middleware
setup_middleware(app)

# Include API v1 Routers with /api/v1 prefix
app.include_router(health.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(evaluation.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

# Root level fallbacks for backward compatibility
app.include_router(health.router)
app.include_router(search.router)
app.include_router(ingest.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
