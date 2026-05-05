# 🤖 Local RAG AI Assistant

A **local Retrieval-Augmented Generation (RAG) chatbot** built with **LangChain, Ollama, and Streamlit**.

This project enables users to upload documents and ask questions, with answers strictly grounded in the provided knowledge base — reducing hallucination and improving reliability.

---

## 📸 Demo

![RAG Demo](screenshot.png)

---

## 🚀 Features

- 📄 Upload TXT / PDF documents  
- 🔍 Semantic search using vector database (Chroma)  
- 🧠 Query rewriting with pronoun resolution  
- 📊 Reranking for improved retrieval quality  
- 🤖 Local LLM (Ollama) for answer generation  
- 🖥️ Interactive UI built with Streamlit  
- 🔒 Strict grounding to prevent hallucination  

---

## 🧱 System Architecture

```
User Question
    ↓
Query Rewrite (Pronoun Resolution)
    ↓
Vector Retrieval (Chroma)
    ↓
Reranking
    ↓
Prompt Construction
    ↓
Local LLM (Ollama)
    ↓
Streamlit UI
```

---

## 🛠️ Tech Stack

- Python  
- LangChain  
- Ollama (Local LLM)  
- Chroma Vector Database  
- Streamlit  
- SentenceTransformers  

---

## 📂 Project Structure

```
rag-chatbot-demo/
├── app/
│   ├── pipeline/
│   │   ├── rewrite.py        # Query rewriting logic
│   │   └── prompt.py         # Prompt construction
│   ├── retrieval/
│   │   ├── retriever.py      # Vector retrieval
│   │   └── reranker.py       # Reranking logic
│   └── utils/
│       └── logger.py         # Logging system
├── vector_dbs/               # Local vector database
├── web_app.py                # Streamlit UI entry
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start local LLM
ollama serve
ollama pull llama3

# Run the app
streamlit run web_app.py
```

---

## 🎯 Key Highlights

- Built a **RAG pipeline from scratch**  
- Implemented **query rewriting with pronoun resolution**  
- Designed a **retrieval + reranking pipeline**  
- Applied **strict grounding to reduce hallucination**  
- Structured code in a **modular, production-like architecture**  

---

## 📌 Future Improvements

- Hybrid query rewriting (rule-based + LLM)  
- Multi-document context reasoning  
- Deployment (Streamlit Cloud / Docker)  
- RAG evaluation metrics (retrieval quality, answer accuracy)  

---

## 👨‍💻 Author

**Zhipeng L