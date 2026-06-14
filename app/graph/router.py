from langgraph.graph import END
from app.graph.state import AgentState

MAX_RETRIES = 3

def tools_router(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

def approval_router(state):
    if state["approved"]:
        return "executor"

    return END

def review_router(state):
    if (
        state["requires_changes"] and
        state["retry_count"] < MAX_RETRIES
    ):
        return "executor"

    return END