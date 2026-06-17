from langchain_core.messages import AIMessage

from app.graph.state import AgentState
from app.services.retrieval import retrieve_context

def analysis_agent_node(state: AgentState):

    query = state["messages"][-1].content

    context = retrieve_context(query)

    return {
        "messages": [
            AIMessage(
                content=f"""
                Retrieved Context:

                {context}
                """
            )
        ]
    }