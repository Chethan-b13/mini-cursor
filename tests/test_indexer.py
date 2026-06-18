from app.services.codebase_indexer import (
    index_codebase,
    search_codebase,
)


index_codebase(".")

# results = search_codebase(
#     "Where is the Ollama model initialized?"
# )

# for result in results:
#     print("=" * 80)
#     print(result.metadata)
#     print(result.page_content[:500])