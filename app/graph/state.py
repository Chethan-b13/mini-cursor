from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from app.schemas.plan import ExecutionPlan

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

    task_type: str

    task_reasoning: str | None

    current_plan: Optional[ExecutionPlan]

    approved: bool

    review_feedback: Optional[str]

    requires_changes: bool

    retry_count: int

    execution_history: list[str]

    last_terminal_output: str | None

    debug_attempts: int