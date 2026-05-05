def retrieve_documents(vectordb, query: str, k: int = 8):
    """
    初始检索：先取较多候选 chunks
    """
    return vectordb.similarity_search(query, k=k)