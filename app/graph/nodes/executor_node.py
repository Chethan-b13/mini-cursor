from langchain_core.messages import SystemMessage

from app.core.llm import llm
from app.prompts.system_prompt import SYSTEM_PROMPT
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

    system_message = SystemMessage(
        content=f"""
        {SYSTEM_PROMPT}

        CURRENT EXECUTION PLAN:
        {plan.model_dump_json(indent=2)}

        RETRIEVED CONTEXT:
        {retrieved_context}

        REVIEWER FEEDBACK:
        {state.get("review_feedback")}

        Follow the approved plan carefully.
        """
    )

    response = llm_with_tools.invoke(
        [system_message] + messages
    )

    return {
        "messages": [response]
    }