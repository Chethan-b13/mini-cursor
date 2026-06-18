from langchain_core.tools import tool
from pathlib import Path
import shutil
from datetime import datetime

BACKUP_DIR = Path(".mini_cursor_backups")

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


def create_backup(file_path: str):
    BACKUP_DIR.mkdir(exist_ok=True)

    source = Path(file_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = BACKUP_DIR / f"{source.name}_{timestamp}"

    shutil.copy(source, backup_path)

    return str(backup_path)

#@deprecated("Use apply_file_patch() instead. This tool will be removed")
@tool
def replace_in_file(
    file_path: str,
    old_text: str,
    new_text: str,
):
    """
    Replace a specific text block inside a file.

    Use this tool when modifying existing code, updating implementations,
    refactoring logic, or patching configuration values.

    The replacement is performed only once (first occurrence only) to avoid
    accidentally modifying multiple matching sections.

    A backup of the original file is created before writing changes.

    Args:
        file_path: Path to the target file.
        old_text: Exact text to locate in the file.
        new_text: Replacement text to insert.

    Returns:
        Success or error message describing the result of the operation.
    """

    try:
        path  = Path(file_path)

        if not path.exists():
            return f"File not found: {file_path}"
        
        content = path.read_text()

        if old_text not in content:
            return "Old text not found in file."
        
        create_backup(file_path)

        updated_content = content.replace(
            old_text,
            new_text,
            1
        )

        path.write_text(updated_content)

        return "Replacement successful."

    except Exception as e:
        return f"Error editing file: {str(e)}"