from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.graph.state import AgentState

from app.graph.nodes.approval_node import approval_node
from app.graph.nodes.executor_node import executor_node, tools
from app.graph.nodes.planner_node import planner_node

from app.graph.router import approval_router, tools_router

graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "planner",
    planner_node
)

graph_builder.add_node(
    "approval",
    approval_node
)

graph_builder.add_node(
    "executor",
    executor_node
)

graph_builder.add_node(
    "tools",
    ToolNode(tools)
)

# EDGES

graph_builder.add_edge(
    START,
    "planner"
)

graph_builder.add_edge(
    "planner",
    "approval"
)

graph_builder.add_conditional_edges(
    "approval",
    approval_router
)

graph_builder.add_conditional_edges(
    "executor",
    tools_router
)

graph_builder.add_edge(
    "tools",
    "executor"
)

graph = graph_builder.compile()