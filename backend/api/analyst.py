from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.analyst_service import analyze_dataset


router = APIRouter()


class AnalystRequest(BaseModel):
    dataset_name: str
    question: str


@router.post("/analyze")

def analyze(request: AnalystRequest):

    result = analyze_dataset(
        request.dataset_name,
        request.question
    )

    return result