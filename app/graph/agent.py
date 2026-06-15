from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState

from app.graph.nodes.analysis_agent_node import analysis_agent_node
from app.graph.nodes.supervisor_node import supervisor_node

from app.graph.router import supervisor_router
from app.graph.subgraphs.editing_subgraph import editing_subgraph
from app.graph.subgraphs.debugging_subgraph import debugging_subgraph


graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "supervisor",
    supervisor_node
)

graph_builder.add_node(
    "analysis_agent",
    analysis_agent_node
)

graph_builder.add_node(
    "editing_agent",
    editing_subgraph
)

graph_builder.add_node(
    "debugging_agent",
    debugging_subgraph
)

# EDGES

graph_builder.add_edge(
    START,
    "supervisor"
)

graph_builder.add_conditional_edges(
    "supervisor",
    supervisor_router
)

graph = graph_builder.compile()