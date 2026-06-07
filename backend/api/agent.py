from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from agents.supervisor_agent import classify_request
from agents.sql_agent import run_sql_agent
from agents.insight_agent import run_insight_agent
from agents.forecast_agent import run_forecast_agent

router = APIRouter()

class AgentRequest(BaseModel):
    dataset_name: str
    question: str
    date_column: Optional[str] = None
    target_column: Optional[str] = None

@router.post("/agent")
def run_agent(request: AgentRequest):
    """
    Main orchestration endpoint that routes requests to specialized AI agents.
    """
    task_type = classify_request(request.question)

    try:
        if "sql_analysis" in task_type:
            result = run_sql_agent(request.dataset_name, request.question)
        elif "insight_generation" in task_type:
            result = run_insight_agent(request.dataset_name)
        elif "forecasting" in task_type:
            result = run_forecast_agent(
                request.dataset_name,
                request.date_column,
                request.target_column,
                request.question
            )
        else:
            result = {
                "status": "error",
                "message": f"No specialized agent configured for task type: {task_type}"
            }

        return {
            "task_type": task_type,
            "result": result
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )