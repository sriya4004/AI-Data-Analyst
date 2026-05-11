from fastapi import APIRouter

from backend.core.dataset_registry import DatasetRegistry

router = APIRouter()


@router.get("/datasets")

def get_datasets():

    return {
        "datasets": DatasetRegistry.list_datasets()
    }