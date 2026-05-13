from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.agents.supervisor_agent import classify_request
from backend.agents.sql_agent import run_sql_agent
from backend.agents.insight_agent import run_insight_agent
from backend.agents.forecast_agent import run_forecast_agent

router = APIRouter()

class AgentRequest(BaseModel):
    dataset_name: str
    question: str
    date_column: Optional[str] = None
    target_column: Optional[str] = None

@router.post("/agent")
def run_agent(request: AgentRequest):
    """
    Main orchestration endpoint that routes user requests to specialized AI agents.
    """
    # 1. Classify the user's intent using the Supervisor Agent
    task_type = classify_request(request.question)

    # 2. Route to the specialized agent based on the classified task type
    try:
        if "sql_analysis" in task_type:
            result = run_sql_agent(
                request.dataset_name,
                request.question
            )

        elif "insight_generation" in task_type:
            result = run_insight_agent(
                request.dataset_name
            )

        elif "forecasting" in task_type:
            # Automatic column detection is handled internally by the Forecast Agent
            result = run_forecast_agent(
                request.dataset_name,
                request.date_column,
                request.target_column,
                request.question
            )

        else:
            # Fallback for unhandled task types
            result = {
                "status": "error",
                "message": f"No specialized agent configured for task type: {task_type}"
            }

        return {
            "task_type": task_type,
            "result": result
        }

    except HTTPException as he:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise he
    except Exception as e:
        # Catch-all for unexpected agent errors
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )