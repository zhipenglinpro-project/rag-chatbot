from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_chat_endpoint_with_mock(monkeypatch):
    def mock_route_query(question: str):
        return {
            "tool_name": "rag_search",
            "answer": "Mock answer",
            "rewritten_query": question,
            "initial_retrieved_chunks": 8,
            "reranked_chunks_used": 3,
            "sources": ["Mock retrieved context"]
        }

    monkeypatch.setattr("backend.main.route_query", mock_route_query)
    ## replace 'backend.main.route_query' with 'mock_route_query'

    response = client.post(
        "/chat",
        json={"question": "What is Chris learning?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Mock answer"
    assert data["tool_name"] == "rag_search"
    assert data["rewritten_query"] == "What is Chris learning?"
    assert data["initial_retrieved_chunks"] == 8
    assert data["reranked_chunks_used"] == 3
    assert data["sources"] == ["Mock retrieved context"]