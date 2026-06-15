from typing import List
from fastapi import FastAPI, UploadFile, File
from backend.schemas import ChatRequest, ChatResponse, UploadResponse, DeleteKnowledgeBaseResponse
from backend.agent.router import route_query
# from backend.rag_pipeline import answer_question
from backend.document_service import load_uploaded_file, build_vector_db_from_documents, delete_latest_vector_db



app = FastAPI(
    title="Local RAG AI Assistant API",
    description="Backend API for RAG chatbot",
    version="1.0.0"
)

@app.delete("/knowledge_base", response_model=DeleteKnowledgeBaseResponse)
def delete_knowledge_base():
    result = delete_latest_vector_db()

    return DeleteKnowledgeBaseResponse(
        message=result["message"],
        deleted=result["deleted"]
    )

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Used to confirm whether the backend server is running.
    """
    return {
        "status": "ok",
        "message": "RAG backend is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint.

    It receives a user question,
    sends it to the RAG pipeline,
    and returns the answer plus retrieval metadata.
    """
    
    result = result = route_query(request.question)

    #result = answer_question(request.question)


    return ChatResponse(
        answer=result.get("answer", ""),
        rewritten_query=result.get("rewritten_query"),
        initial_retrieved_chunks=result.get("initial_retrieved_chunks", 0),
        reranked_chunks_used=result.get("reranked_chunks_used", 0),
        sources=result.get("sources", []),
        tool_name=result.get("tool_name")
    )

@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload one or multiple TXT/PDF files and build a new vector database.
    """
    all_documents = []

    for file in files:
        file_bytes = await file.read()

        documents = load_uploaded_file(
            file_bytes=file_bytes,
            filename=file.filename
        )

        all_documents.extend(documents)

    if not all_documents:
        return UploadResponse(
            message="No readable content found in uploaded files.",
            document_count=0,
            chunk_count=0,
            db_path=""
        )

    result = build_vector_db_from_documents(all_documents)

    return UploadResponse(
        message="Knowledge base built successfully.",
        document_count=result["document_count"],
        chunk_count=result["chunk_count"],
        db_path=result["db_path"]
    )