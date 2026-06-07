from workflows.analyst_workflow import analyst_graph
from agents.visualization_agent import run_visualization_agent

def run_sql_agent(dataset_name, question):
    """
    Executes the SQL analysis workflow and generates a corresponding visualization.
    """
    initial_state = {
        "dataset_name": dataset_name,
        "user_question": question
    }

    workflow_result = analyst_graph.invoke(initial_state)

    visualization_result = run_visualization_agent(
        question,
        workflow_result["query_result"]
    )

    workflow_result.update(visualization_result)
    return workflow_result