from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.services.codebase_indexer import search_codebase


class CodebaseRetrievalInput(BaseModel):
    query: str = Field(
        description="The precise search query, keywords, or code symbols to look up in the codebase."
    )
    k: Optional[int] = Field(
        default=5, 
        description="The maximum number of highly relevant file chunks to retrieve."
    )


@tool("retrieve_codebase_context", args_schema=CodebaseRetrievalInput)
def retrieve_codebase_context(query: str, k: int = 5) -> str:
    """Search and retrieve raw source code snippets and context from the codebase backend.
    
    Use this tool whenever you need specific details about files, classes, functions, 
    or implementation structures to answer questions or formulate accurate coding plans.
    """
    try:
        print("ToolCall: retrieve_codebase_context")
        results = search_codebase(query, k=k)
        if not results:
            return "No matching codebase context found for the given query."

        context_parts = []
        for result in results:
            source = result.metadata.get("source", "Unknown Source File")
            snippet = result.page_content.strip()
            
            # Formatted cleanly with clear delineations for LLM consumption
            context_parts.append(f"--- FILE: {source} ---\n{snippet}")

        print("ToolCall (DONE): retrieve_codebase_context")
        return "\n\n".join(context_parts)
        
    except Exception as e:
        return f"Error retrieving codebase context: {str(e)}"