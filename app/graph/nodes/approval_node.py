
from app.graph.state import AgentState

def approval_node(state: AgentState):
    approval = input(
        "\nApprove plan? (yes/no): "
    )

    return {
        "approved": approval.lower() == "yes"
    }