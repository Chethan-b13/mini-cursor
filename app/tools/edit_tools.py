from pathlib import Path
import shutil
from datetime import datetime
from langchain_core.tools import tool

BACKUP_DIR = Path(".mini_cursor_backups")

def create_backup(file_path: str):
    BACKUP_DIR.mkdir(exist_ok=True)

    source = Path(file_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = BACKUP_DIR / f"{source.name}_{timestamp}"

    shutil.copy(source, backup_path)

    return str(backup_path)


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