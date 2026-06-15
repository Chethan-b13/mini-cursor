from langchain_core.prompts import ChatPromptTemplate

DEBUG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert debugging engineer.

        Your job:
        - analyze runtime failures
        - identify probable root causes
        - determine fix strategy

        Focus heavily on:
        - stack traces
        - terminal output
        - execution failures
        """
    ),
    (
        "human",
        """
        USER REQUEST:
        {request}

        TERMINAL OUTPUT:
        {terminal_output}
        """
    )
])