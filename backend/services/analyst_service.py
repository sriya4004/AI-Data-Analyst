from backend.core.dataset_registry import DatasetRegistry
from backend.services.data_loader import DataLoader
from backend.services.llm_service import generate_response


def analyze_dataset(dataset_name: str, user_query: str):

    df = DatasetRegistry.get_dataset(dataset_name)

    if df is None:
        return {
            "error": "Dataset not found"
        }

    schema = DataLoader.get_schema(df)

    preview = DataLoader.get_preview(df)

    prompt = f"""
    You are an AI Data Analyst.

    Dataset Name:
    {dataset_name}

    Dataset Schema:
    {schema}

    Dataset Preview:
    {preview}

    User Question:
    {user_query}

    Answer the user's question accurately using the dataset information.
    """

    response = generate_response(prompt)

    return {
        "dataset": dataset_name,
        "question": user_query,
        "response": response
    }