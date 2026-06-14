from backend.vector_store import retrieve_documents
from backend.llm_factory import get_llm


def summary_tool(question: str = "Summarize the uploaded knowledge base.") -> dict:
    """
    Summary Tool.

    This tool summarizes the uploaded knowledge base based on retrieved chunks.
    It is useful when the user asks for a summary instead of asking a specific factual question.
    """

    docs = retrieve_documents(question, k=8)

    if not docs:
        return {
            "tool_name": "summary",
            "answer": "No knowledge base found or no relevant content available for summarization.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a document summarization assistant.

Summarize the following knowledge base content clearly and concisely.

Rules:
- Use only the provided content.
- Do not add outside information.
- Focus on the main topics and key points.
- Keep the summary concise.

Content:
{context}

Summary:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "tool_name": "summary",
        "answer": response.content.strip(),
        "sources": [doc.page_content for doc in docs]
    }