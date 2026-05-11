from fastapi import APIRouter
from pydantic import BaseModel

from backend.core.duckdb_instance import duckdb_instance


router = APIRouter()


class SQLQuery(BaseModel):
    query: str


@router.post("/query")

def run_query(request: SQLQuery):

    result = duckdb_instance.run_query(request.query)

    return {
        "query": request.query,
        "result": result
    }