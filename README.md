# 🤖 Local RAG AI Assistant

A local Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Ollama, and Streamlit.

It allows users to upload documents and ask questions, with answers grounded strictly in the provided knowledge base.

---

## 🚀 Features

- 📄 Upload TXT / PDF documents
- 🔍 Semantic search using vector database (Chroma)
- 🧠 Query rewriting with pronoun resolution
- 📊 Reranking for better retrieval quality
- 🤖 Local LLM (Ollama) for answer generation
- 🖥️ Interactive UI built with Streamlit
- 🔒 Strict grounding (no hallucination)

---

## 🧱 System Architecture

User Question
↓
Query Rewrite (resolve pronouns)
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
---

## 🛠️ Tech Stack

- Python
- LangChain
- Ollama (Local LLM)
- Chroma Vector DB
- Streamlit
- SentenceTransformers

---

## 📂 Project Structure

rag-chatbot-demo/
├── app/
│   ├── pipeline/
│   │   ├── rewrite.py
│   │   └── prompt.py
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── reranker.py
│   └── utils/
│       └── logger.py
├── vector_dbs/
├── web_app.py
├── requirements.txt
└── README.md

---

## ⚙️ How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

ollama serve
ollama pull llama3

streamlit run web_app.py

🎯 Key Highlights

* Implemented a RAG pipeline from scratch
* Built a query rewriting module with pronoun resolution
* Designed a retrieval + reranking pipeline
* Enforced strict grounding to prevent hallucination
* Structured code in a modular, production-like architecture

📸 Demo

(Add a screenshot here later)

⸻

📌 Future Improvements

* Better query rewriting (LLM-based hybrid)
* Multi-document context handling
* Deployment (Streamlit Cloud / Docker)
* Evaluation metrics (RAG quality)

👨‍💻 Author

Zhipeng Lin

