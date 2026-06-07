from fastapi import FastAPI

from backend.core.config import settings
from backend.api.upload import router as upload_router
from backend.api.datasets import router as dataset_router
from backend.api.insights import router as insights_router
from backend.api.workflow import (
    router as workflow_router
)
from backend.api.agent import router as agent_router

app = FastAPI(
    title="AI Data Analyst Agent",
    description="AI-powered analytics platform",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(dataset_router)
app.include_router(insights_router)
app.include_router(workflow_router)
app.include_router(agent_router)

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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)