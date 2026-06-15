# planner should only think not act 
#  thats why its a service not a tool 

from app.prompts.editing_subgraph_prompts import PLANNER_PROMPT

from app.core.llm import llm
from app.schemas.plan import ExecutionPlan


planner_llm = llm.with_structured_output(
    ExecutionPlan
)

def create_plan(task: str, retrieved_context: str):
    chain = PLANNER_PROMPT | planner_llm

    result = chain.invoke({
        "task": task,
        "retrieved_context": retrieved_context
    })

    return result