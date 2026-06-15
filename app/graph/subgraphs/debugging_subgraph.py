from langgraph.graph import (
    StateGraph,
    START,
    END,
)
from app.graph.state import AgentState
from app.graph.nodes.debug_terminal_node import debug_terminal_node
from app.graph.nodes.debug_planner_node import debug_planner_node
from app.graph.subgraphs.editing_subgraph import editing_subgraph


debug_graph_builder = StateGraph(AgentState)

debug_graph_builder.add_node(
    "terminal",
    debug_terminal_node
)

debug_graph_builder.add_node(
    "debug_planner",
    debug_planner_node
)

debug_graph_builder.add_node(
    "editing_agent",
    editing_subgraph
)

# EDGES

debug_graph_builder.add_edge(
    START,
    "terminal"
)

debug_graph_builder.add_edge(
    "terminal",
    "debug_planner"
)

debug_graph_builder.add_edge(
    "debug_planner",
    "editing_agent"
)

debug_graph_builder.add_edge(
    "editing_agent",
    END
)

debugging_subgraph = (
    debug_graph_builder.compile()
)