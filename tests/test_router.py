from backend.agent.router import route_query


def test_route_to_summary():
    result = route_query("summarize this document")

    assert result["tool_name"] == "summary"


def test_route_to_keyword():
    result = route_query("what are the key topics?")

    assert result["tool_name"] == "keyword"


def test_route_to_metadata():
    result = route_query("what tools are available?")

    assert result["tool_name"] == "metadata"


def test_route_to_rag():
    result = route_query("who is chris?")

    assert result["tool_name"] == "rag_search"