from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".idea",
    "chroma_db",
    ".chroma"
}

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".md",
}

def scan_codebase(root_path: str):
    root = Path(root_path)

    files = []

    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        if path.suffix in SUPPORTED_EXTENSIONS:
            files.append(path)

    return files

def chunk_code(content: str, chunk_size: int = 1500):

    lines = content.splitlines()

    chunks = []

    current_chunk = []

    current_length = 0

    for line in lines:
        current_chunk.append(line)
        current_length += len(line)

        if current_length >= chunk_size:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk: 
        chunks.append("\n".join(current_chunk))

    return chunks

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_store = Chroma(
    collection_name="codebase",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def index_codebase(root_path: str):
    files = scan_codebase(root_path)

    documents = []

    for file_path in files:
        try:
            content = file_path.read_text()

            chunks = chunk_code(content)

            for i, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": str(file_path),
                            "chunk": i
                        }
                    )
                )
        
        except Exception as ex:
            print(f"Failed to process {file_path}: {ex}")

    vector_store.add_documents(documents)

    print(f"Indexed {len(documents)} chunks")

def search_codebase(query: str, k: int = 5):
    results = vector_store.similarity_search(
        query, 
        k=k
    )

    return results