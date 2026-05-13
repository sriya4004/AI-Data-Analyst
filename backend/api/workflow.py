from fastapi import APIRouter
from pydantic import BaseModel
from backend.workflows.analyst_workflow import analyst_graph

router = APIRouter()

class WorkflowRequest(BaseModel):
    dataset_name: str
    question: str

@router.post("/workflow-analysis")
def workflow_analysis(request: WorkflowRequest):
    """
    Directly invokes the analyst workflow graph for a given dataset and question.
    """
    initial_state = {
        "dataset_name": request.dataset_name,
        "user_question": request.question
    }
    return analyst_graph.invoke(initial_state)