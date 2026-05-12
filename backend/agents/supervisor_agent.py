from backend.services.llm_service import generate_response


SQL_KEYWORDS = [
    "average",
    "sum",
    "count",
    "group",
    "highest",
    "lowest",
    "trend",
    "compare",
    "distribution",
    "show",
    "calculate"
]

INSIGHT_KEYWORDS = [
    "insight",
    "summary",
    "analyze",
    "overview",
    "patterns",
    "anomalies"
]

FORECAST_KEYWORDS = [
    "forecast",
    "predict",
    "future",
    "projection"
]


def classify_request(user_question: str):

    question = user_question.lower()

    # RULE-BASED ROUTING FIRST

    if any(word in question for word in FORECAST_KEYWORDS):

        return "forecasting"

    if any(word in question for word in SQL_KEYWORDS):

        return "sql_analysis"

    if any(word in question for word in INSIGHT_KEYWORDS):

        return "insight_generation"

    # FALLBACK TO LLM

    prompt = f"""
    You are an AI supervisor agent.

    Classify the request into ONE category:

    - sql_analysis
    - visualization
    - insight_generation
    - forecasting

    User Request:
    {user_question}

    Return ONLY the category name.
    """

    response = generate_response(prompt)

    return response.strip().lower()