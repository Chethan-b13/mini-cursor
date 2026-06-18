from pathlib import Path
from typing import Tuple

from app.schemas.file_patch import FilePatch, PatchResult
from app.tools.file_tools import create_backup


def validate_patch(patch: FilePatch) -> Tuple[bool, str]:
    """Validate if the patch line boundaries fit the target file."""
    path = Path(patch.file_path)
    if not path.is_file():
        return False, f"File not found: {patch.file_path}"

    try:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        total_lines = len(lines)
    except (UnicodeDecodeError, PermissionError) as e:
        return False, f"Cannot read file: {e}"

    if patch.start_line < 1 or patch.end_line > total_lines or patch.start_line > patch.end_line:
        return False, f"Invalid line range {patch.start_line}-{patch.end_line}. File has {total_lines} lines."

    return True, "Valid patch"


def apply_patch(patch: FilePatch) -> PatchResult:
    """Apply a validated patch to the file safely."""
    path = Path(patch.file_path)
    
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    
    # Extract base indentation from the first line being replaced
    # This ensures replacement code inherits the correct indentation
    base_indentation = ""
    if patch.start_line <= len(lines):
        original_line = lines[patch.start_line - 1]
        # Extract leading whitespace
        stripped = original_line.lstrip()
        if stripped:  # Only if line has non-whitespace content
            base_indentation = original_line[:len(original_line) - len(stripped)]
    
    # Format replacement code to ensure it matches the layout
    replacement_lines = patch.replacement_code.splitlines(keepends=True)
    
    # Apply base indentation to replacement lines that don't already have it
    # This handles cases where LLM provides "temperature=0.2" instead of "    temperature=0.2"
    normalized_replacement = []
    for i, line in enumerate(replacement_lines):
        stripped_line = line.lstrip()
        if stripped_line:  # Only add indentation to non-empty lines
            # If line has no leading whitespace, add the base indentation
            if line and line[0] not in (' ', '\t'):
                normalized_replacement.append(base_indentation + line)
            else:
                normalized_replacement.append(line)
        else:
            # Preserve blank lines as-is
            normalized_replacement.append(line)
    
    # Ensure last line ends with newline if replacement_code did
    if normalized_replacement and patch.replacement_code.endswith("\n"):
        if not normalized_replacement[-1].endswith("\n"):
            normalized_replacement[-1] += "\n"
    
    # Slice-replace (convert 1-based index to 0-based index)
    lines[patch.start_line - 1 : patch.end_line] = normalized_replacement

    # Create backup and write changes atomically
    create_backup(patch.file_path)
    path.write_text("".join(lines), encoding="utf-8")

    return PatchResult(
        success=True,
        message="Patch applied successfully.",
        file_path=patch.file_path,
    )