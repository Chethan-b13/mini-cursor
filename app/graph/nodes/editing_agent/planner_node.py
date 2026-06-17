from app.graph.state import AgentState
from app.services.planner import create_plan
from app.services.retrieval import retrieve_context

def planner_node(state: AgentState):

    user_request = state["messages"][-1].content
    retrieved_context = retrieve_context(user_request)

    plan = create_plan(user_request, retrieved_context)

    print("\n========== PLAN ==========")
    print(plan.model_dump_json(indent=2))
    print("==========================\n")

    return {
        "current_plan": plan,
        "execution_history": [],
        "retry_count": 0,
    }