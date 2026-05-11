from fastapi import APIRouter

from backend.services.insight_service import (
    generate_dataset_insights
)

router = APIRouter()


@router.get("/generate-insights")

def generate_insights(dataset_name: str):

    result = generate_dataset_insights(dataset_name)

    return result