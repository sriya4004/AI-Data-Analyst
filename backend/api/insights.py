from fastapi import APIRouter
from services.insight_service import generate_dataset_insights

router = APIRouter()

@router.get("/generate-insights")
def generate_insights(dataset_name: str):
    """
    Endpoint for generating analytical insights for a specific dataset.
    """
    return generate_dataset_insights(dataset_name)