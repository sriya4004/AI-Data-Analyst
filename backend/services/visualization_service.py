import json

from backend.services.llm_service import generate_response


def generate_chart_config(user_question, query_result):

    prompt = f"""
    You are a data visualization expert.

    Based on the user's analytical question and SQL query result,
    determine the BEST chart type.

    Available chart types:
    - bar
    - line
    - pie
    - scatter

    User Question:
    {user_question}

    Query Result:
    {query_result}

    Return ONLY valid JSON in this format:

    {{
        "chart_type": "bar",
        "x_column": "placement",
        "y_column": "average_iq"
    }}
    """

    response = generate_response(prompt)

    response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        response_json = json.loads(response)

        return response_json

    except Exception:

        return {
            "chart_type": "bar",
            "x_column": "",
            "y_column": ""
        }