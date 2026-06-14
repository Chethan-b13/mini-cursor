from langchain_core.tools import tool
from pathlib import Path


@tool
def read_file(file_path: str) -> str:
    """
    Load the contents of a file for code analysis and editing tasks.

    This tool should be used before making code changes or answering
    questions about implementation details. It helps the agent inspect:
    - functions
    - classes
    - imports
    - configs
    - tests
    - application flow

    Prefer using this tool before attempting:
    - code modifications
    - bug fixes
    - refactoring
    - feature additions
    - architecture explanations

    Args:
        file_path: Path to the target file.

    Returns:
        The full text contents of the file, or an error message if the
        file does not exist or cannot be read.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"Error: The file '{file_path}' does not exist."
        
        return path.read_text()
        
    except Exception as e:
        return f"Error: An error occurred while checking the file path: {str(e)}"
    
@tool
def list_files(directory: str = "."):
    """
    Recursively scan a directory and return visible project files.

    Useful for:
    - exploring unfamiliar codebases
    - locating implementation files
    - identifying configs, tests, and entry points
    - understanding repository structure before code edits

    Hidden files and hidden directories are automatically ignored.

    Args:
        directory: Directory to scan recursively. Defaults to current directory.

    Returns:
        Newline-separated relative file paths (maximum 200 results).
    """

    try:
        root = Path(directory)

        files = []

        for path in root.rglob("*"):
            if any(part.startswith(".") for part in path.parts):
                continue

            if path.is_file():
                files.append(str(path))


        return "\n".join(files[:200])
    
    except Exception as e:
        return f"Error listing files: {str(e)}" 