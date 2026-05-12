from backend.services.insight_service import (
    generate_dataset_insights
)


def run_insight_agent(dataset_name):

    return generate_dataset_insights(dataset_name)