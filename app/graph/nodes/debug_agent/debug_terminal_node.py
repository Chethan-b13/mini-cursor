from app.graph.state import AgentState
from app.tools.terminal_tools import (
    run_terminal_command,
)


def debug_terminal_node(state: AgentState):

    result = run_terminal_command.invoke({
        "command": "pytest"
    })

    print("\n======= TERMINAL OUTPUT =======")
    print(result)
    print("================================\n")

    return {
        "last_terminal_output": result
    }