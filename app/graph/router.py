from langgraph.graph import END
from app.graph.state import AgentState

MAX_RETRIES = 3

def editing_tools_router(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

def editing_approval_router(state):
    if state["approved"]:
        return "editing_agent"

    return END

def editing_review_router(state):
    if (
        state["requires_changes"] and
        state["retry_count"] < MAX_RETRIES
    ):
        return "editing_agent"

    return END

def supervisor_router(state):
    task_type = state["task_type"]

    if task_type == "analysis":
        return "analysis_agent"

    if task_type == "editing":
        return "editing_agent"

    if task_type == "debugging":
        return "debugging_agent"

    if task_type == "refactoring":
        return "editing_agent"

    return "analysis_agent"