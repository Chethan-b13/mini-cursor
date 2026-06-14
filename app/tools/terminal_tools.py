import subprocess

from langchain_core.tools import tool

@tool
def run_terminal_command(command: str):
    """
    Run a terminal command in the project directory.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return f"""
            STDOUT:
            {result.stdout}

            STDERR:
            {result.stderr}

            RETURN CODE:
            {result.returncode}
        """

    except Exception as e:
        return f"Terminal execution error: {str(e)}" 