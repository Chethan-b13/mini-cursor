from app.graph.state import AgentState

from app.services.debug_planner import (
    create_debug_plan,
)


def debug_planner_node(state: AgentState):

    request = state["messages"][-1].content

    terminal_output = state.get(
        "last_terminal_output",
        ""
    )

    plan = create_debug_plan(
        request,
        terminal_output,
    )

    print("\n======= DEBUG PLAN =======")
    print(plan.model_dump_json(indent=2))
    print("==========================\n")

    return {
        "current_plan": plan
    }