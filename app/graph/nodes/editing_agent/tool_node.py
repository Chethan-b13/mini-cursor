from langgraph.prebuilt import ToolNode
from app.tools.file_tools import read_file, list_files
from app.tools.patch_tools import apply_file_patch
from app.tools.terminal_tools import run_terminal_command
from app.tools.codebase_context_tool import retrieve_codebase_context

# Exposed tools for LLM to use during execution
tools = [
    read_file,
    apply_file_patch,
    list_files,
    run_terminal_command,
    retrieve_codebase_context
]


editing_tool_node = ToolNode(tools)