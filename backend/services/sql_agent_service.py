from backend.core.dataset_registry import DatasetRegistry
from backend.core.duckdb_instance import duckdb_instance

from backend.services.data_loader import DataLoader
from backend.services.llm_service import generate_response
from backend.services.visualization_service import generate_chart_config

def ai_sql_analysis(dataset_name: str, user_question: str):

    df = DatasetRegistry.get_dataset(dataset_name)

    if df is None:
        return {
            "error": "Dataset not found"
        }

    schema = DataLoader.get_schema(df)

    table_name = dataset_name.split(".")[0]

    sql_prompt = f"""
    You are an expert SQL analyst.

    Dataset table name:
    {table_name}

    Dataset schema:
    {schema}

    Generate ONLY a valid DuckDB SQL query.

    User Question:
    {user_question}

    Return ONLY SQL query.
    """

    generated_sql = generate_response(sql_prompt)

    generated_sql = generated_sql.strip().replace("```sql", "").replace("```", "")

    try:

        query_result = duckdb_instance.run_query(generated_sql)
        chart_config = generate_chart_config(
        user_question,
        query_result
        )

    except Exception as e:

        return {
            "error": str(e),
            "generated_sql": generated_sql
        }

    insight_prompt = f"""
    You are a business analyst.

    User Question:
    {user_question}

    SQL Query:
    {generated_sql}

    Query Result:
    {query_result}

    Generate clear analytical insights from the query result.
    """

    final_response = generate_response(insight_prompt)

    return {
        "dataset": dataset_name,
        "question": user_question,
        "generated_sql": generated_sql,
        "query_result": query_result,
        "chart_config": chart_config,
        "analysis": final_response
    }