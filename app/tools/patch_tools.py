from langchain_core.tools import tool

from app.schemas.file_patch import FilePatch
from app.services.patching_service import validate_patch, apply_patch


@tool
def apply_file_patch(
    file_path: str,
    start_line: int,
    end_line: int,
    replacement_code: str,
):
    """
    Apply a file patch using 1-based line indices.

    IMPORTANT: For maintaining proper indentation:
    - You can provide replacement_code with OR without leading whitespace
    - The tool will automatically inherit indentation from the first line being replaced
    - This is useful for single-line changes where you only provide the new content
    
    Examples:
    
    Example 1 - Single line change (indentation auto-applied):
    - Original: "    temperature=0" (4 spaces)
    - Provide: "temperature=0.2" (tool adds 4 spaces automatically)
    - Result: "    temperature=0.2" ✓
    
    Example 2 - Multi-line change (provide full indentation):
    - Original lines:
        llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL"),
        )
    - Start: 1, End: 3
    - Provide:
        llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL"),
            temperature=0.2,
        )

    Args:
        file_path: Path to the file to modify.
        start_line: 1-based start line of the text to replace.
        end_line: 1-based end line of the text to replace (inclusive).
        replacement_code: Replacement text to insert. Can have or omit indentation.

    Returns:
        A success or error message.
    """
    print(f"ToolCall: apply_file_patch {file_path} {start_line} {end_line} \n\n replacement_code={replacement_code}")
    patch = FilePatch(
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        replacement_code=replacement_code,
        reasoning="Applied via apply_file_patch tool",
    )

    is_valid, validation_message = validate_patch(patch)
    if not is_valid:
        return f"Error: {validation_message}"

    result = apply_patch(patch)
    if not result.success:
        return f"Error applying patch: {result.message}"

    print("ToolCall (DONE): apply_file_patch")
    return f"Patch applied successfully to {file_path}."
