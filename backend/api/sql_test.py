from fastapi import APIRouter
import pandas as pd

from backend.tools.duckdb_tool import DuckDBTool

router = APIRouter()

duckdb_tool = DuckDBTool()


@router.get("/test-sql")

def test_sql():

    data = {
        "month": ["Jan", "Feb", "Mar"],
        "revenue": [1000, 2000, 3000]
    }

    df = pd.DataFrame(data)

    duckdb_tool.register_dataframe("sales", df)

    query = """
    SELECT
        month,
        revenue
    FROM sales
    """

    result = duckdb_tool.run_query(query)

    return {
        "query_result": result
    }