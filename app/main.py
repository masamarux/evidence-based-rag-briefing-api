from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.cases import router as cases_router
from app.api.routes.sources import router as sources_router


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(cases_router)
app.include_router(sources_router)

@app.get("/")
def root():
    return {
        "message": settings.app_name,
        "environment": settings.app_env,
        "docs": "/docs",
    }
