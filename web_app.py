import os
import shutil
import tempfile
import uuid

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.pipeline.rewrite import rewrite_query
from app.retrieval.retriever import retrieve_documents
from app.retrieval.reranker import rerank_documents
from app.pipeline.prompt import build_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)

VECTOR_DB_ROOT = "vector_dbs"

logger.info("running web_app.py")
# print("DEBUG: running web_app.py")

st.set_page_config(page_title="Local RAG AI Assistant", page_icon="🤖")
st.title("🤖 Local RAG AI Assistant")
st.write("Upload files and ask questions about your knowledge base.")


# ---------------------------
# 缓存基础资源
# ---------------------------

@st.cache_resource
def load_embedding():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


@st.cache_resource
def load_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0
    )


@st.cache_resource
def load_vectordb(db_path: str):
    embeddings = load_embedding()
    return Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )


# ---------------------------
# 通用函数
# ---------------------------

def ensure_vector_root():
    os.makedirs(VECTOR_DB_ROOT, exist_ok=True)


def load_uploaded_documents(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        suffix = os.path.splitext(uploaded_file.name)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            if suffix == ".txt":
                loader = TextLoader(tmp_path, encoding="utf-8")
                documents.extend(loader.load())

            elif suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)
                documents.extend(loader.load())

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    return documents


def build_vector_db(documents):
    ensure_vector_root()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    embeddings = load_embedding()

    new_db_path = os.path.join(VECTOR_DB_ROOT, str(uuid.uuid4()))

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=new_db_path
    )

    return new_db_path, len(chunks)


def delete_directory_if_exists(path: str):
    if path and os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def format_chat_history(messages, max_turns=3):
    """
    仍然保留聊天历史字符串，用于最终回答 prompt。
    rewrite 已经不再依赖它来提取 subject。
    """
    if not messages:
        return ""

    recent_messages = messages[-max_turns * 2:]

    history_lines = []
    for msg in recent_messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        history_lines.append(f"{role}: {content}")

    return "\n".join(history_lines)


# ---------------------------
# Session 初始化
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_db_path" not in st.session_state:
    st.session_state.current_db_path = None

if "vectordb_ready" not in st.session_state:
    st.session_state.vectordb_ready = False

if "latest_subject" not in st.session_state:
    st.session_state.latest_subject = None


# ---------------------------
# 侧边栏
# ---------------------------

with st.sidebar:
    st.header("Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload TXT or PDF files",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if st.session_state.vectordb_ready and st.session_state.current_db_path:
        st.success("Knowledge base loaded")
        st.caption(f"Current DB: {st.session_state.current_db_path}")
        st.caption(f"Latest subject: {st.session_state.latest_subject}")
    else:
        st.info("No active knowledge base")

    if st.button("Build Knowledge Base"):
        if not uploaded_files:
            st.warning("Please upload at least one TXT or PDF file.")
        else:
            with st.spinner("Reading files and building knowledge base..."):
                documents = load_uploaded_documents(uploaded_files)

                if not documents:
                    st.error("No readable content found in uploaded files.")
                else:
                    new_db_path, chunk_count = build_vector_db(documents)

                    st.session_state.current_db_path = new_db_path
                    st.session_state.vectordb_ready = True
                    st.session_state.messages = []
                    st.session_state.latest_subject = None

                    st.cache_resource.clear()

                    st.success(
                        f"Knowledge base built successfully! "
                        f"Loaded {len(documents)} documents and created {chunk_count} chunks."
                    )

                    st.rerun()

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.latest_subject = None
        st.rerun()

    if st.button("Delete Current Knowledge Base"):
        old_path = st.session_state.current_db_path

        st.cache_resource.clear()
        delete_directory_if_exists(old_path)

        st.session_state.current_db_path = None
        st.session_state.vectordb_ready = False
        st.session_state.messages = []
        st.session_state.latest_subject = None

        st.success("Current knowledge base deleted.")
        st.rerun()


# ---------------------------
# 加载 LLM
# ---------------------------

llm = load_llm()


# ---------------------------
# 渲染历史聊天
# ---------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            if "rewritten_query" in message and message["rewritten_query"]:
                st.caption(f"Rewritten query: {message['rewritten_query']}")

            if "initial_result_count" in message:
                st.caption(f"Initial retrieved chunks: {message['initial_result_count']}")

            if "result_count" in message:
                st.caption(f"Reranked chunks used: {message['result_count']}")

            if message.get("context"):
                with st.expander("Retrieved Context"):
                    st.write(message["context"])


# ---------------------------
# 聊天输入
# ---------------------------

question = st.chat_input("Ask something about your documents...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    if not st.session_state.vectordb_ready or not st.session_state.current_db_path:
        answer = "Please upload files and click 'Build Knowledge Base' first."
        context = ""
        result_count = 0
        initial_result_count = 0
        rewritten_query = question

    else:
        vectordb = load_vectordb(st.session_state.current_db_path)

        with st.spinner("Rewriting query, retrieving, reranking, and generating answer..."):
            # 1. 仅用于最终回答，不再用于提取 subject
            chat_history = format_chat_history(
                st.session_state.messages[:-1],
                max_turns=3
            )

            # 2. Query Rewrite（基于 latest_subject）
            rewritten_query, st.session_state.latest_subject = rewrite_query(
                question,
                st.session_state.latest_subject
            )

            # print("DEBUG question =", question)
            # print("DEBUG rewritten_query =", rewritten_query)
            # print("DEBUG latest_subject =", st.session_state.latest_subject)

            # 3. 初始检索
            initial_results = retrieve_documents(vectordb, rewritten_query, k=8)
            initial_result_count = len(initial_results)

            if initial_result_count == 0:
                context = ""
                answer = "No relevant information found in the knowledge base. Try rephrasing your question."
                result_count = 0
            else:
                # 4. Rerank
                results, scored_docs = rerank_documents(
                    rewritten_query,
                    initial_results,
                    llm,
                    top_k=3
                )
                result_count = len(results)

                # 5. 组装 context
                context = "\n\n".join([doc.page_content for doc in results])

                # 6. 最终回答仍然基于原问题
                prompt = build_prompt(question, context, chat_history)
                response = llm.invoke(prompt)
                answer = response.content.strip()

    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption(f"Rewritten query: {rewritten_query}")
        st.caption(f"Initial retrieved chunks: {initial_result_count}")
        st.caption(f"Reranked chunks used: {result_count}")

        if context:
            with st.expander("Retrieved Context"):
                st.write(context)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "context": context,
        "result_count": result_count,
        "initial_result_count": initial_result_count,
        "rewritten_query": rewritten_query
    })