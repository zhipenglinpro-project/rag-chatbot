from backend.vector_store import get_latest_vector_db_path


def metadata_tool() -> dict:
    """
    Metadata Tool.

    This tool returns basic system and knowledge base metadata.
    It is useful when the user asks:
    - What is the current knowledge base?
    - Is a knowledge base loaded?
    - What tools are available?
    """

    db_path = get_latest_vector_db_path()

    if not db_path:
        kb_status = "No active knowledge base found."
    else:
        kb_status = f"Active knowledge base path: {db_path}"

    return {
        "tool_name": "metadata",
        "answer": (
            f"{kb_status}\n\n"
            "Available tools:\n"
            "- rag_search: answer factual questions using the knowledge base\n"
            "- summary: summarize the uploaded knowledge base\n"
            "- keyword: extract key topics and keywords\n"
            "- metadata: show system and knowledge base metadata"
        ),
        "sources": []
    }