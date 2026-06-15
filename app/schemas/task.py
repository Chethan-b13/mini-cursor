from enum import Enum

from pydantic import BaseModel


class TaskType(str, Enum):
    ANALYSIS = "analysis"
    EDITING = "editing"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"


class TaskClassification(BaseModel):
    task_type: TaskType
    reasoning: str