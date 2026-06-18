import os
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path so `app` package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.file_patch import FilePatch
from app.services.patching_service import validate_patch, apply_patch
from app.tools.file_tools import create_backup


def test_apply_and_backup(tmp_path, monkeypatch):
    # create a temporary file to patch
    file = tmp_path / "sample.txt"
    original = "line1\nSEARCH_ME\nline3\n"
    file.write_text(original)

    # change cwd to tmp_path so backups are created inside tmp dir
    monkeypatch.chdir(tmp_path)

    patch = FilePatch(
        file_path=str(file),
        start_line=2,
        end_line=2,
        replacement_code="REPLACED\n",
        reasoning="test"
    )

    # validator should accept the patch
    valid, msg = validate_patch(patch)
    assert valid, msg

    # apply the patch
    result = apply_patch(patch)
    assert result.success is True

    # file content should be updated
    updated = file.read_text()
    assert "REPLACED" in updated
    assert "SEARCH_ME" not in updated

    # backup dir should exist and contain a backup for the file
    backup_dir = Path(".mini_cursor_backups")
    assert backup_dir.exists()
    backups = list(backup_dir.iterdir())
    assert any(b.name.startswith(file.name + "_") for b in backups)


def test_apply_file_patch_tool(tmp_path, monkeypatch):
    file = tmp_path / "sample.txt"
    file.write_text("line1\nSEARCH_ME\nline3\n")
    monkeypatch.chdir(tmp_path)

    patch = FilePatch(
        file_path=str(file),
        start_line=2,
        end_line=2,
        replacement_code="REPLACED\n",
        reasoning="test"
    )
    
    is_valid, msg = validate_patch(patch)
    assert is_valid, msg
    
    result = apply_patch(patch)
    assert result.success

    assert "SEARCH_ME" not in file.read_text()
    backup_dir = Path(".mini_cursor_backups")
    assert backup_dir.exists()
    assert any(b.name.startswith(file.name + "_") for b in backup_dir.iterdir())


def test_indentation_preservation_single_line(tmp_path, monkeypatch):
    """Test that indentation is preserved when replacing a single indented line"""
    file = tmp_path / "test.py"
    file.write_text("def foo():\n    temperature=0\n    return True\n")
    monkeypatch.chdir(tmp_path)

    # Replace with content that has NO leading spaces
    # The tool should automatically apply the 4-space indent from the original line
    patch = FilePatch(
        file_path=str(file),
        start_line=2,
        end_line=2,
        replacement_code="temperature=0.2\n",
        reasoning="test"
    )
    
    apply_patch(patch)

    result = file.read_text()
    assert "    temperature=0.2" in result
    assert "temperature=0.2)" not in result  # Should NOT lose indent or close paren on same line
    assert result == "def foo():\n    temperature=0.2\n    return True\n"


def test_indentation_preservation_multiline(tmp_path, monkeypatch):
    """Test LLM example: update temperature in ChatOllama function call"""
    file = tmp_path / "llm.py"
    original = """llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0
)
"""
    file.write_text(original)
    monkeypatch.chdir(tmp_path)

    # Replace just the temperature line without leading spaces
    patch = FilePatch(
        file_path=str(file),
        start_line=4,
        end_line=4,
        replacement_code="temperature=0.2\n",
        reasoning="test"
    )
    
    apply_patch(patch)

    result = file.read_text()
    expected = """llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0.2
)
"""
    assert result == expected
    assert "temperature=0.2)" not in result  # Should NOT close paren on same line
    assert "temperature=0\n" not in result  # Old value should be gone (exact line match)


def test_indentation_with_tabs(tmp_path, monkeypatch):
    """Test indentation preservation with tab characters"""
    file = tmp_path / "test.py"
    file.write_text("def foo():\n\ttemp=0\n\treturn True\n")
    monkeypatch.chdir(tmp_path)

    patch = FilePatch(
        file_path=str(file),
        start_line=2,
        end_line=2,
        replacement_code="temp=100\n",
        reasoning="test"
    )
    
    apply_patch(patch)

    result = file.read_text()
    assert "\ttemp=100" in result
    assert result == "def foo():\n\ttemp=100\n\treturn True\n"


def test_multiline_replacement_with_explicit_indent(tmp_path, monkeypatch):
    """Test multi-line replacement where indentation is explicitly provided"""
    file = tmp_path / "test.py"
    original = """if True:
    x = 1
    y = 2
"""
    file.write_text(original)
    monkeypatch.chdir(tmp_path)

    # Replace multiple lines with explicit indentation
    patch = FilePatch(
        file_path=str(file),
        start_line=2,
        end_line=3,
        replacement_code="    x = 10\n    y = 20\n",
        reasoning="test"
    )
    
    apply_patch(patch)

    result = file.read_text()
    assert "    x = 10" in result
    assert "    y = 20" in result
    assert "x = 1\n" not in result  # Old value should be gone
    assert "y = 2\n" not in result  # Old value should be gone
