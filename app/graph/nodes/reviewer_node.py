import json
from pydantic import BaseModel

from app.core.llm import llm
from app.prompts.editing_subgraph_prompts import REVIEW_PROMPT


class ReviewResult(BaseModel):
    requires_changes: bool
    feedback: str


reviewer_llm = llm.with_structured_output(
    ReviewResult
)


def normalize_history_entry(entry):
    if isinstance(entry, str):
        return entry
    if hasattr(entry, "content"):
        return str(entry.content)
    if isinstance(entry, list):
        return "\n".join(normalize_history_entry(item) for item in entry)
    return json.dumps(entry, indent=2)


def reviewer_node(state):
    request = state["messages"][0].content

    plan = state["current_plan"]

    result = state["messages"][-1].content

    execution_history_list = state.get("execution_history", [])
    if not isinstance(execution_history_list, list):
        execution_history_list = [execution_history_list]

    execution_history = "\n".join(
        normalize_history_entry(item)
        for item in execution_history_list
    )

    chain =  REVIEW_PROMPT | reviewer_llm

    review = chain.invoke({
        "request": request,
        "plan": plan.model_dump_json(indent=2),
        "result": result,
        "execution_history": execution_history
    })

    print("\n========== REVIEW ==========")
    print(review.model_dump_json(indent=2))
    print("============================\n")

    return {
        "review_feedback": review.feedback,
        "requires_changes": review.requires_changes,
        "retry_count": state.get("retry_count", 0) + 1
    }