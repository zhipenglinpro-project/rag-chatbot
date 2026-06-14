from backend.vector_store import retrieve_documents
from backend.llm_factory import get_llm


def keyword_tool(question: str = "Extract key topics from the uploaded knowledge base.") -> dict:
    """
    Keyword Tool.

    This tool extracts key topics and keywords from the uploaded knowledge base.
    It is useful when the user asks:
    - What are the key topics?
    - List the main keywords.
    - What is this document mainly about?
    """

    docs = retrieve_documents(question, k=8)

    if not docs:
        return {
            "tool_name": "keyword",
            "answer": "No knowledge base found or no relevant content available for keyword extraction.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a keyword extraction assistant.

Extract the main topics and keywords from the following knowledge base content.

Rules:
- Use only the provided content.
- Do not add outside information.
- Return 5 to 10 concise keywords or short phrases.
- Use bullet points.

Content:
{context}

Keywords:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "tool_name": "keyword",
        "answer": response.content.strip(),
        "sources": [doc.page_content for doc in docs]
    }