from pydantic import BaseModel
from typing import List

class DebugPlan(BaseModel):
    root_cause: str
    suspected_files: List[str]
    fix_strategy: str