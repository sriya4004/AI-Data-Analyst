from fastapi import FastAPI

from backend.core.config import settings
from backend.api.upload import router as upload_router
from backend.api.sql_test import router as sql_router
from backend.api.datasets import router as dataset_router
from backend.api.query import router as query_router
from backend.api.ai_test import router as ai_router
from backend.api.analyst import router as analyst_router
from backend.api.ai_sql import router as ai_sql_router
from backend.api.insights import router as insights_router

app = FastAPI(
    title="AI Data Analyst Agent",
    description="AI-powered analytics platform",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(sql_router)
app.include_router(dataset_router)
app.include_router(query_router)
app.include_router(ai_router)
app.include_router(analyst_router)
app.include_router(ai_sql_router)
app.include_router(insights_router)

@app.get("/")
def root():
    return {
        "message": "AI Data Analyst Backend Running",
        "model": settings.MODEL_NAME
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }