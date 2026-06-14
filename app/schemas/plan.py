from pydantic import BaseModel
from typing import List


class PlanStep(BaseModel):
    step_number: int
    description: str


class ExecutionPlan(BaseModel):
    objective: str
    files_to_inspect: List[str]
    steps: List[PlanStep]
    risks: List[str]