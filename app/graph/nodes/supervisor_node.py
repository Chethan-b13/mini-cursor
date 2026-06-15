from app.services.supervisor import classify_task
from app.graph.state import AgentState


def supervisor_node(state: AgentState):

    request = state["messages"][-1].content

    classification = classify_task(request)

    print("\n======= TASK CLASSIFICATION =======")
    print(classification.model_dump_json(indent=2))
    print("===================================\n")

    return {
        "task_type": classification.task_type,
        "task_reasoning": classification.reasoning,
    }