from fastapi import APIRouter
from pydantic import BaseModel

from backend.agents.supervisor_agent import (
    classify_request
)

from backend.agents.sql_agent import (
    run_sql_agent
)

from backend.agents.insight_agent import (
    run_insight_agent
)


router = APIRouter()


class AgentRequest(BaseModel):

    dataset_name: str
    question: str


@router.post("/agent")

def run_agent(request: AgentRequest):

    task_type = classify_request(
        request.question
    )

    if "sql_analysis" in task_type:

        result = run_sql_agent(
            request.dataset_name,
            request.question
        )

    elif "insight_generation" in task_type:

        result = run_insight_agent(
            request.dataset_name
        )

    else:

        result = {
            "message": f"No specialized agent yet for: {task_type}"
        }

    return {
        "task_type": task_type,
        "result": result
    }