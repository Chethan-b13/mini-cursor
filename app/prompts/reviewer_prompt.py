from langchain_core.prompts import ChatPromptTemplate


REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior software reviewer.

        Your job:
        - inspect the execution result
        - detect mistakes
        - detect incomplete implementations
        - verify the plan was followed

        Be strict and technical.

        Only approve if the task appears correctly completed.
        If the assistant reports tool usage, check that the evidence supports each claimed edit.
        """
    ),
    (
        "human",
        """
        USER REQUEST:
        {request}

        EXECUTION PLAN:
        {plan}

        EXECUTION RESULT:
        {result}

        EXECUTION HISTORY:
        {execution_history}
        """
    )
])