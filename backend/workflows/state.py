from typing import TypedDict, Optional


class AnalystState(TypedDict):

    dataset_name: str

    user_question: str

    schema: Optional[dict]

    generated_sql: Optional[str]

    query_result: Optional[list]

    analysis: Optional[str]

    chart_config: Optional[dict]