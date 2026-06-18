from app.core.llm import llm
from app.prompts.editing_subgraph_prompts import EDITING_EXECUTOR_PROMPT
from app.graph.nodes.editing_agent.tool_node import tools

llm_with_tools = llm.bind_tools(tools)


def executor_node(state):
    """
    Execute code edits using an LLM with tool access.
    
    The node:
    1. Prepares the prompt with task, plan, and feedback
    2. Invokes LLM with tool bindings (read_file, apply_file_patch, etc.)
    3. Tracks execution history for review
    4. Returns response and updated history
    
    The service layer (editing_service) handles patch generation and validation
    when structured patching is needed.
    """
    messages = state["messages"]
    user_request = messages[-1].content
    plan = state.get("current_plan")
    raw_history = state.get("execution_history", [])
    
    if not isinstance(raw_history, list):
        raw_history = [raw_history]

    # Prepare the prompt with context
    prompt_value = EDITING_EXECUTOR_PROMPT.invoke({
        "task": user_request,
        "plan": plan.model_dump_json(indent=2),
        "review_feedback": state.get("review_feedback", ""),
        "execution_history": "\n".join(str(item) for item in raw_history),
    })

    # Invoke LLM with tool access
    response = llm_with_tools.invoke(
        prompt_value.to_messages() + messages
    )

    # Update execution history
    updated_history = raw_history
    updated_history.append(
        response.content if isinstance(response.content, str) else str(response.content)
    )

    return {
        "messages": [response],
        "execution_history": updated_history,
    }