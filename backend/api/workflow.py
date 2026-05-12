from fastapi import APIRouter
from pydantic import BaseModel

from backend.workflows.analyst_workflow import (
    analyst_graph
)

router = APIRouter()


class WorkflowRequest(BaseModel):

    dataset_name: str
    question: str


@router.post("/workflow-analysis")

def workflow_analysis(request: WorkflowRequest):

    initial_state = {
        "dataset_name": request.dataset_name,
        "user_question": request.question
    }

    result = analyst_graph.invoke(initial_state)

    return result