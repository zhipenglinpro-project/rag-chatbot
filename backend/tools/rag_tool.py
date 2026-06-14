from backend.rag_pipeline import answer_question


def rag_search_tool(question: str) -> dict:
    """
    RAG Search Tool.

    This tool answers user questions based on the uploaded knowledge base.
    It reuses the existing RAG pipeline:
    - query rewrite
    - vector retrieval
    - reranking
    - prompt construction
    - LLM generation
    """

    result = answer_question(question)

    return {
        "tool_name": "rag_search",
        "answer": result["answer"],
        "rewritten_query": result["rewritten_query"],
        "initial_retrieved_chunks": result["initial_retrieved_chunks"],
        "reranked_chunks_used": result["reranked_chunks_used"],
        "sources": result["sources"]
    }