from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.sql_agent_service import ai_sql_analysis


router = APIRouter()


class SQLAgentRequest(BaseModel):
    dataset_name: str
    question: str


@router.post("/ai-sql")

def analyze_with_sql(request: SQLAgentRequest):

    result = ai_sql_analysis(
        request.dataset_name,
        request.question
    )

    return result