import os
import shutil
import tempfile
import uuid

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.vector_store import get_embedding_model, VECTOR_DB_ROOT


def load_uploaded_file(file_bytes: bytes, filename: str):
    """
    Load uploaded TXT or PDF file into LangChain documents.
    """
    suffix = os.path.splitext(filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    try:
        if suffix == ".txt":
            loader = TextLoader(tmp_path, encoding="utf-8")
            return loader.load()

        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
            return loader.load()

        return []

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def build_vector_db_from_documents(documents):
    """
    Split documents, generate embeddings, and save them into a new Chroma DB folder.
    """
    os.makedirs(VECTOR_DB_ROOT, exist_ok=True)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    new_db_path = os.path.join(VECTOR_DB_ROOT, str(uuid.uuid4()))

    Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        persist_directory=new_db_path
    )

    return {
        "db_path": new_db_path,
        "document_count": len(documents),
        "chunk_count": len(chunks)
    }