from langchain_core.tools import tool
from pathlib import Path


@tool
def read_file(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"Error: The file '{file_path}' does not exist."
        
        return path.read_text()
        
    except Exception as e:
        return f"Error: An error occurred while checking the file path: {str(e)}"