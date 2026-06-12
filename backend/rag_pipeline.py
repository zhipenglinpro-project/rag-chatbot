from langchain_ollama import ChatOllama

from backend.vector_store import retrieve_documents
from app.pipeline.rewrite import rewrite_query
from app.pipeline.prompt import build_prompt
from app.retrieval.reranker import rerank_documents
from backend.llm_factory import get_llm


latest_subject = None



def answer_question(question: str) -> dict:
    """
    Full RAG pipeline for FastAPI backend:
    1. query rewrite
    2. vector retrieval
    3. rerank
    4. prompt construction
    5. local LLM answer generation
    """

    global latest_subject

    llm = get_llm()

    rewritten_query, latest_subject = rewrite_query(
        question,
        latest_subject
    )

    initial_docs = retrieve_documents(rewritten_query, k=8)

    if not initial_docs:
        return {
            "answer": "No relevant information found in the knowledge base.",
            "rewritten_query": rewritten_query,
            "initial_retrieved_chunks": 0,
            "reranked_chunks_used": 0,
            "sources": []
        }

    reranked_docs, scored_docs = rerank_documents(
        rewritten_query,
        initial_docs,
        llm,
        top_k=3
    )

    context = "\n\n".join([doc.page_content for doc in reranked_docs])

    # FastAPI 版本暂时不传完整 chat history，先保持单轮稳定。
    chat_history = ""

    prompt = build_prompt(
        question=rewritten_query,
        context=context,
        chat_history=chat_history
    )

    response = llm.invoke(prompt)
    answer = response.content.strip()

    return {
        "answer": answer,
        "rewritten_query": rewritten_query,
        "initial_retrieved_chunks": len(initial_docs),
        "reranked_chunks_used": len(reranked_docs),
        "sources": [doc.page_content for doc in reranked_docs]
    }