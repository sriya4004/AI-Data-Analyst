import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.data_loader import DataLoader
from core.dataset_registry import DatasetRegistry
from core.duckdb_instance import duckdb_instance

router = APIRouter()
UPLOAD_DIR = "backend/uploads"
ALLOWED_EXTENSIONS = [".csv", ".xlsx"]

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file uploads, cleans the dataset, and registers it with the platform.
    """
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = DataLoader.load_dataset(file_path)
    df, cleaning_report = DataLoader.clean_dataset(df)
    
    DatasetRegistry.register_dataset(file.filename, df)
    table_name = file.filename.split(".")[0].replace("-", "_").replace(" ", "_")
    duckdb_instance.register_dataframe(table_name, df)
    
    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "cleaning_report": cleaning_report,
        "dataset_info": DataLoader.get_basic_info(df),
        "schema": DataLoader.get_schema(df),
        "preview": DataLoader.get_preview(df),
        "registered_datasets": DatasetRegistry.list_datasets(),
    }