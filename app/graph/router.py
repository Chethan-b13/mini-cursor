from langgraph.graph import END
from app.graph.state import AgentState

def tools_router(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

def approval_router(state):
    if state["approved"]:
        return "executor"

    return END