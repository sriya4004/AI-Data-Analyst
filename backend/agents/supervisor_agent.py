from services.llm_service import generate_response

INTENT_REGISTRY = {
    "forecasting": [
        "forecast", "predict", "future", "projection", 
        "sales prediction", "revenue prediction"
    ],
    "sql_analysis": [
        "average", "sum", "count", "group", "highest", "lowest",
        "trend", "compare", "distribution", "show", "calculate",
        "chart", "graph", "plot", "visualize", "visualization"
    ],
    "insight_generation": [
        "insight", "summary", "analyze", "overview", 
        "patterns", "anomalies"
    ]
}

def classify_request(user_question: str) -> str:
    """
    Classifies the user's question into a task category using rule-based
    matching with an LLM fallback.
    """
    question = user_question.lower()

    for task_type, keywords in INTENT_REGISTRY.items():
        if any(keyword in question for keyword in keywords):
            return task_type

    prompt = f"""
    You are an AI supervisor agent for a multi-agent analytics platform.

    Classify the user's request into EXACTLY ONE of these categories:
    - sql_analysis (calculating values, grouping data, finding extremes)
    - visualization (creating charts, plots, or graphs)
    - insight_generation (summarizing findings, detecting patterns/anomalies)
    - forecasting (predicting future trends, sales, or metrics)

    User Request:
    {user_question}

    Return ONLY the category name in lowercase.
    """

    try:
        response = generate_response(prompt)
        return response.strip().lower()
    except Exception:
        return "sql_analysis"