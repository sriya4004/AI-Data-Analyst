from backend.services.visualization_service import (
    generate_chart_config
)


def run_visualization_agent(
    user_question,
    query_result
):

    chart_config = generate_chart_config(
        user_question,
        query_result
    )

    return {
        "chart_config": chart_config
    }