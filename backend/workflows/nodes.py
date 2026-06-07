from core.dataset_registry import DatasetRegistry
from services.data_loader import DataLoader
from services.llm_service import generate_response
from core.duckdb_instance import duckdb_instance
from services.kpi_service import (
    extract_kpis
)


def schema_node(state):

    df = DatasetRegistry.get_dataset(
        state["dataset_name"]
    )

    schema = DataLoader.get_schema(df)

    state["schema"] = schema

    return state


def sql_generation_node(state):

    table_name = state["dataset_name"].split(".")[0]

    prompt = f"""
    You are an expert SQL analyst.

    Dataset table:
    {table_name}

    Schema:
    {state["schema"]}

    Generate ONLY a valid DuckDB SQL query.

    User Question:
    {state["user_question"]}
    """

    sql = generate_response(prompt)

    sql = (
        sql
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    state["generated_sql"] = sql

    return state


def sql_execution_node(state):

    result = duckdb_instance.run_query(
        state["generated_sql"]
    )

    state["query_result"] = result

    return state


def insight_node(state):

    kpis = extract_kpis(
        state["query_result"]
    )

    prompt = f"""
    You are an expert business analyst.

    User Question:
    {state["user_question"]}

    Query Result:
    {state["query_result"]}

    Computed KPIs:
    {kpis}

    IMPORTANT:
    - ONLY use provided metrics
    - DO NOT invent statistics
    - DO NOT hallucinate numbers

    Generate grounded business insights.
    """

    analysis = generate_response(prompt)

    state["analysis"] = analysis

    return state