from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    """
    Request body for /chat endpoint.
    """
    question: str


class ChatResponse(BaseModel):
    """
    Response body for /chat endpoint.
    """
    answer: str
    rewritten_query: Optional[str] = None
    initial_retrieved_chunks: int = 0
    reranked_chunks_used: int = 0
    sources: List[str] = []
    tool_name: str | None = None

class UploadResponse(BaseModel):
    """
    Response body for /upload endpoint.
    """
    message: str
    document_count: int
    chunk_count: int
    db_path: str