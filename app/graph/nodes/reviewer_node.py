from pydantic import BaseModel

from app.core.llm import llm
from app.prompts.reviewer_prompt import REVIEW_PROMPT


class ReviewResult(BaseModel):
    requires_changes: bool
    feedback: str


reviewer_llm = llm.with_structured_output(
    ReviewResult
)

def reviewer_node(state):
    request = state["messages"][0].content

    plan = state["current_plan"]

    result = state["messages"][-1].content

    chain =  REVIEW_PROMPT | reviewer_llm

    review = chain.invoke({
        "request": request,
        "plan": plan.model_dump_json(indent=2),
        "result": result
    })

    print("\n========== REVIEW ==========")
    print(review.model_dump_json(indent=2))
    print("============================\n")

    return {
        "review_feedback": review.feedback,
        "requires_changes": review.requires_changes,
    }