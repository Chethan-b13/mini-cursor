from pydantic import BaseModel


class FilePatch(BaseModel):
    file_path: str

    start_line: int

    end_line: int

    replacement_code: str

    reasoning: str


class PatchResult(BaseModel):
    success: bool

    message: str

    file_path: str