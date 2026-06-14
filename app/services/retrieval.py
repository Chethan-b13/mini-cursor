from app.services.codebase_indexer import search_codebase



def retrieve_context(query: str, k: int = 5):
    results = search_codebase(query, k=k)

    context_parts = []

    for result in results:
        source = result.metadata.get("source")

        context_parts.append(
            f"""
            FILE: {source}

            {result.page_content}
            """
        )
    
    return "\n\n".join(context_parts)