from fastapi import APIRouter
from core.dataset_registry import DatasetRegistry

router = APIRouter()

@router.get("/datasets")
def get_datasets():
    """
    Returns a list of all registered datasets.
    """
    return {"datasets": DatasetRegistry.list_datasets()}