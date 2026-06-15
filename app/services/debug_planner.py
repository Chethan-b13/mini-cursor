from app.prompts.debugging_subgraph_prompts import DEBUG_PROMPT

from app.core.llm import llm
from app.schemas.debug import DebugPlan

debug_planner_llm = llm.with_structured_output(
    DebugPlan
)

def create_debug_plan(
    request: str,
    terminal_output: str,
):
    chain = DEBUG_PROMPT | debug_planner_llm

    return chain.invoke({
        "request": request,
        "terminal_output": terminal_output,
    })