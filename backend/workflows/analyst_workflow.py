from langgraph.graph import StateGraph, END

from backend.workflows.state import AnalystState
from backend.workflows.nodes import (
    schema_node,
    sql_generation_node,
    sql_execution_node,
    insight_node,
)

workflow = StateGraph(AnalystState)

workflow.add_node(
    "schema_node",
    schema_node
)

workflow.add_node(
    "sql_generation_node",
    sql_generation_node
)

workflow.add_node(
    "sql_execution_node",
    sql_execution_node
)

workflow.add_node(
    "insight_node",
    insight_node
)

workflow.set_entry_point("schema_node")

workflow.add_edge(
    "schema_node",
    "sql_generation_node"
)

workflow.add_edge(
    "sql_generation_node",
    "sql_execution_node"
)

workflow.add_edge(
    "sql_execution_node",
    "insight_node"
)

workflow.add_edge(
    "insight_node",
    END
)

analyst_graph = workflow.compile()