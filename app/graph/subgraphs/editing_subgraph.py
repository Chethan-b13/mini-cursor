from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.graph.nodes.approval_node import approval_node
from app.graph.nodes.planner_node import planner_node
from app.graph.nodes.editing_agent_node import editing_agent_node
from app.graph.nodes.reviewer_node import reviewer_node
from app.graph.nodes.tool_nodes import editing_tool_node
from app.graph.router import (
    editing_approval_router, 
    editing_review_router, 
    editing_tools_router,
)
from app.graph.state import AgentState


editing_graph_builder = StateGraph(AgentState)


editing_graph_builder.add_node(
    "planner",
    planner_node
)

editing_graph_builder.add_node(
    "approval",
    approval_node
)

editing_graph_builder.add_node(
    "editing_agent",
    editing_agent_node
)

editing_graph_builder.add_node(
    "tools",
    editing_tool_node
)

editing_graph_builder.add_node(
    "reviewer",
    reviewer_node
)


# EDGES

editing_graph_builder.add_edge(
    START,
    "planner"
)

editing_graph_builder.add_edge(
    "planner",
    "approval"
)

editing_graph_builder.add_conditional_edges(
    "approval",
    editing_approval_router
)

editing_graph_builder.add_conditional_edges(
    "editing_agent",
    editing_tools_router,
    {
        "tools": "tools",
        END: "reviewer"
    }
)

editing_graph_builder.add_conditional_edges(
    "reviewer",
    editing_review_router
)

editing_graph_builder.add_edge(
    "tools",
    "editing_agent"
)



editing_subgraph = (
    editing_graph_builder.compile()
)