import requests
import streamlit as st
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Local RAG AI Assistant", page_icon="🤖")

st.title("🤖 Local RAG AI Assistant")
st.write("Frontend connected to FastAPI backend.")


# ---------------------------
# Sidebar: Upload document
# ---------------------------

with st.sidebar:
    st.header("Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload TXT or PDF file",
        type=["txt", "pdf"]
    )

    if st.button("Upload and Build Knowledge Base"):
        if uploaded_file is None:
            st.warning("Please upload a TXT or PDF file first.")
        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            with st.spinner("Uploading file and building knowledge base..."):
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files=files
                )

            if response.status_code == 200:
                result = response.json()
                st.success(result["message"])
                st.write(f"Documents: {result['document_count']}")
                st.write(f"Chunks: {result['chunk_count']}")
            else:
                st.error("Upload failed.")
                st.write(response.text)


# ---------------------------
# Chat UI
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            if message.get("tool_name"):
                st.caption(f"Tool used: {message['tool_name']}")

            if message.get("rewritten_query"):
                st.caption(f"Rewritten query: {message['rewritten_query']}")

            if "initial_retrieved_chunks" in message:
                st.caption(
                    f"Initial retrieved chunks: {message['initial_retrieved_chunks']}"
                )

            if "reranked_chunks_used" in message:
                st.caption(
                    f"Reranked chunks used: {message['reranked_chunks_used']}"
                )

            if message.get("sources"):
                with st.expander("Retrieved Context"):
                    for i, source in enumerate(message["sources"], start=1):
                        st.markdown(f"**Source {i}:**")
                        st.write(source)


question = st.chat_input("Ask something about your documents...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Sending question to backend..."):
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"question": question}
        )

    if response.status_code == 200:
        result = response.json()

        answer = result["answer"]

        with st.chat_message("assistant"):
            st.markdown(answer)

            if result.get("tool_name"):
                st.caption(f"Tool used: {result['tool_name']}")

            st.caption(f"Rewritten query: {result['rewritten_query']}")
            st.caption(
                f"Initial retrieved chunks: {result['initial_retrieved_chunks']}"
            )
            st.caption(
                f"Reranked chunks used: {result['reranked_chunks_used']}"
            )

            if result["sources"]:
                with st.expander("Retrieved Context"):
                    for i, source in enumerate(result["sources"], start=1):
                        st.markdown(f"**Source {i}:**")
                        st.write(source)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "tool_name": result["tool_name"],
            "rewritten_query": result["rewritten_query"],
            "initial_retrieved_chunks": result["initial_retrieved_chunks"],
            "reranked_chunks_used": result["reranked_chunks_used"],
            "sources": result["sources"]
        })

    else:
        with st.chat_message("assistant"):
            st.error("Backend request failed.")
            st.write(response.text)