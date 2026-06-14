from backend.tools.rag_tool import rag_search_tool
from backend.tools.summary_tool import summary_tool
from backend.tools.keyword_tool import keyword_tool
from backend.tools.metadata_tool import metadata_tool


def route_query(question: str) -> dict:
    """
    Simple rule-based agent router.

    It selects the most appropriate tool based on the user's question.
    """

    q = question.lower()

    # Metadata / system status questions
    if any(keyword in q for keyword in [
        "metadata",
        "system status",
        "knowledge base loaded",
        "tools available",
        "available tools",
        "what tools",
        "current knowledge base"
    ]):
        return metadata_tool()

    # Summary questions
    if any(keyword in q for keyword in [
        "summarize",
        "summary",
        "overview",
        "briefly explain",
        "main idea"
    ]):
        return summary_tool(question)

    # Keyword / topic extraction questions
    if any(keyword in q for keyword in [
        "keyword",
        "keywords",
        "key topics",
        "main topics",
        "topics",
        "key points"
    ]):
        return keyword_tool(question)

    # Default: factual document QA
    return rag_search_tool(question)