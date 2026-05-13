import json
from backend.services.llm_service import generate_response

def generate_chart_config(user_question, query_result):
    """
    Suggests the best chart configuration based on the user's question and query results.
    """
    prompt = f"""
    You are a data visualization expert. Determine the BEST chart type (bar, line, pie, scatter).

    User Question: {user_question}
    Query Result: {query_result}

    Return ONLY JSON:
    {{
        "chart_type": "bar",
        "x_column": "placement",
        "y_column": "average_iq"
    }}
    """

    response = generate_response(prompt).replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(response)
    except Exception:
        return {
            "chart_type": "bar",
            "x_column": "",
            "y_column": ""
        }