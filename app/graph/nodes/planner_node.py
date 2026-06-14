from app.graph.state import AgentState
from app.services.planner import create_plan

def planner_node(state: AgentState):

    user_request = state["messages"][-1].content

    plan = create_plan(user_request)

    print("\n========== PLAN ==========")
    print(plan.model_dump_json(indent=2))
    print("==========================\n")

    return {
        "current_plan": plan
    }