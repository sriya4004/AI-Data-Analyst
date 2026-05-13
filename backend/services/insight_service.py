from backend.core.dataset_registry import DatasetRegistry
from backend.services.data_loader import DataLoader
from backend.services.llm_service import generate_response

def generate_dataset_insights(dataset_name: str):
    """
    Generates high-level business insights from the dataset's schema, metadata, and preview.
    """
    df = DatasetRegistry.get_dataset(dataset_name)
    if df is None:
        return {"error": "Dataset not found"}

    schema = DataLoader.get_schema(df)
    preview = DataLoader.get_preview(df)
    basic_info = DataLoader.get_basic_info(df)

    prompt = f"""
    You are an expert business intelligence analyst.
    Analyze the dataset and generate key insights, trends, anomalies, and KPI observations.

    Dataset: {dataset_name}
    Info: {basic_info}
    Schema: {schema}
    Preview: {preview}

    Return structured analytical insights.
    """

    insights = generate_response(prompt)

    return {
        "dataset": dataset_name,
        "dataset_info": basic_info,
        "insights": insights
    }