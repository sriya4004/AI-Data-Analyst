from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from backend.services.data_loader import DataLoader
from backend.core.dataset_registry import DatasetRegistry
from backend.core.duckdb_instance import duckdb_instance

router = APIRouter()

UPLOAD_DIR = "backend/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".csv", ".xlsx"]


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_extension = os.path.splitext(file.filename)[1]

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = DataLoader.load_dataset(file_path)
    df, cleaning_report = DataLoader.clean_dataset(df)
    
    DatasetRegistry.register_dataset(file.filename, df)
    table_name = file.filename.split(".")[0]
    duckdb_instance.register_dataframe(table_name, df)
    
    preview = DataLoader.get_preview(df)

    schema = DataLoader.get_schema(df)

    basic_info = DataLoader.get_basic_info(df)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "cleaning_report": cleaning_report,
        "dataset_info": basic_info,
        "schema": schema,
        "preview": preview,
        "registered_datasets": DatasetRegistry.list_datasets(),
    }