import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


VECTOR_DB_ROOT = "vector_dbs"


def get_embedding_model():
    """
    Load the same embedding model used to build the vector database.
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


def get_latest_vector_db_path() -> str | None:
    """
    Get the latest vector database folder from vector_dbs/.
    This is a temporary approach for Phase 1.
    Later, we can manage multiple knowledge bases more formally.
    """
    if not os.path.exists(VECTOR_DB_ROOT):
        return None

    db_folders = [
        os.path.join(VECTOR_DB_ROOT, folder)
        for folder in os.listdir(VECTOR_DB_ROOT)
        if os.path.isdir(os.path.join(VECTOR_DB_ROOT, folder))
    ]

    if not db_folders:
        return None

    return max(db_folders, key=os.path.getmtime)


def load_vector_store():
    """
    Load the latest Chroma vector database.
    """
    db_path = get_latest_vector_db_path()

    if not db_path:
        return None

    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )


def retrieve_documents(query: str, k: int = 8):
    """
    Retrieve relevant documents from the latest vector database.
    """
    vectordb = load_vector_store()

    if vectordb is None:
        return []

    return vectordb.similarity_search(query, k=k)