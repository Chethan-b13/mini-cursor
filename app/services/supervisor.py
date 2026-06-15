from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import llm
from app.schemas.task import TaskClassification

from langchain_core.prompts import ChatPromptTemplate

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an orchestration supervisor.

        Your ONLY job is to classify the user's request.

        Do NOT solve the task.

        Choose the BEST task type:
        - analysis
        - editing
        - debugging
        - refactoring

        Classification should be conservative and precise.
        """
    ),
    (
        "human",
        "{request}"
    )
])

supervisor_llm = llm.with_structured_output(
    TaskClassification
)

def classify_task(request: str):
    chain = SUPERVISOR_PROMPT | supervisor_llm

    return chain.invoke({
        "request": request
    })