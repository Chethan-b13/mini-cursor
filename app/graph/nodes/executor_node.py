from langchain_core.messages import SystemMessage

from app.core.llm import llm
from app.prompts.executor_prompt import EXECUTOR_PROMPT
from app.services.retrieval import retrieve_context

from app.tools.file_tools import read_file, list_files
from app.tools.edit_tools import replace_in_file
from app.tools.terminal_tools import run_terminal_command



tools = [
    read_file,
    replace_in_file,
    list_files,
    run_terminal_command
]


llm_with_tools = llm.bind_tools(tools)


def executor_node(state):
    messages = state["messages"]

    user_request = messages[-1].content

    retrieved_context = retrieve_context(user_request)

    plan = state.get("current_plan")

    raw_history = state.get("execution_history", [])
    if not isinstance(raw_history, list):
        raw_history = [raw_history]

    prompt_value = EXECUTOR_PROMPT.invoke({
        "task": user_request,
        "plan": plan.model_dump_json(indent=2),
        "retrieved_context": retrieved_context,
        "review_feedback": state.get("review_feedback", ""),
        "execution_history": "\n".join(
            str(item) for item in raw_history
        )
    })

    response = llm_with_tools.invoke(
        prompt_value.to_messages() + messages
    )

    # update operational memory

    updated_history = raw_history
    updated_history.append(
        response.content if isinstance(response.content, str) else str(response.content)
    )

    return {
        "messages": [response],
        "execution_history": updated_history, # operational memory.
    }