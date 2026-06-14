# 🤖 Local RAG AI Assistant

A production-style local Retrieval-Augmented Generation (RAG) AI Assistant built with LangChain, FastAPI, Ollama, Streamlit, and Docker.

The system supports document-based question answering, intelligent tool selection, and modular AI service architecture.

It enables users to upload documents and interact with a Multi-tool AI Agent that can answer questions, summarize documents, extract keywords, and provide knowledge base metadata.

---

## 📸 Demo

![RAG Demo](screenshot.png)

---

## 🚀 Features

- 📄 Upload TXT / PDF documents
- 🔍 Semantic search using Chroma Vector Database
- 🧠 Query rewriting with pronoun resolution
- 📊 Reranking for improved retrieval accuracy
- 🤖 Local LLM integration using Ollama (Llama 3.2)
- 🧰 Multi-tool AI Agent architecture
  - RAG Search Tool
  - Document Summary Tool
  - Keyword Extraction Tool
  - Metadata Tool
- ⚙️ FastAPI backend with RESTful APIs
- 🖥️ Streamlit frontend
- 🐳 Dockerized frontend and backend services
- 🔒 Strict grounding to reduce hallucination 

---

## 🧱 System Architecture

```text

User
↓
Streamlit Frontend
↓ HTTP Request
FastAPI Backend
↓
Agent Router
├── RAG Search Tool
│       ↓
│   Query Rewrite
│       ↓
│   Chroma Retrieval
│       ↓
│   Reranking
│       ↓
│   LLM Generation
│
├── Summary Tool
│       ↓
│   LLM Summarization
│
├── Keyword Tool
│       ↓
│   Keyword Extraction
│
└── Metadata Tool
        ↓
    System Information
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

```text

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
├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── rag_pipeline.py
│   ├── vector_store.py
│   ├── document_service.py
│   └── llm_factory.py
├── frontend_app.py
├── web_app.py
├── requirements.txt
├── screenshot.png
└── README.md
```

---

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- LangChain
- RESTful API Design

### AI & RAG

- Ollama (Local LLM - Llama 3.2)
- SentenceTransformers
- Chroma Vector Database
- Retrieval-Augmented Generation (RAG)
- Query Rewriting
- Reranking
- Multi-tool Agent Architecture

### Frontend

- Streamlit
- HTTP Requests

### DevOps & Engineering

- Docker
- Docker Compose
- Environment Variable Management
- Modular Service Architecture

---

## 📂 Project Structure

```text
rag-chatbot-demo/
│
├── backend/
│   ├── agent/
│   │   └── router.py             # Tool selection logic
│   │
│   ├── tools/
│   │   ├── rag_tool.py           # Knowledge-based QA
│   │   ├── summary_tool.py       # Document summarization
│   │   ├── keyword_tool.py       # Keyword extraction
│   │   └── metadata_tool.py      # System metadata
│   │
│   ├── main.py                   # FastAPI application
│   ├── schemas.py                # API request/response models
│   ├── rag_pipeline.py           # Core RAG workflow
│   ├── vector_store.py           # Chroma management
│   ├── document_service.py       # File processing & chunking
│   └── llm_factory.py            # LLM provider abstraction
│
├── frontend_app.py               # Streamlit frontend
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
│
├── requirements.txt              # Development dependencies
├── requirements.docker.txt       # Docker runtime dependencies
│
├── vector_dbs/
├── data/
│
├── .dockerignore
├── .env
├── screenshot.png
└── README.md
```

---

## 🔌 API Endpoints

```text
GET  /health
POST /chat
POST /upload
```

---

### POST /chat

Example Request:

```json
{
  "question": "What are the key topics in this document?"
}
```

Example Response:

```json
{
  "tool_name": "keyword",
  "answer": "The main topics are...",
  "rewritten_query": null,
  "initial_retrieved_chunks": 8,
  "reranked_chunks_used": 3,
  "sources": [
    "Retrieved document content..."
  ]
}
```

---

### POST /upload

Upload a TXT or PDF file.

The backend will:

1. Parse the document
2. Split it into chunks
3. Generate embeddings
4. Store vectors in Chroma
5. Build a new knowledge base

---

## ⚙️ Local Development Setup

### 1. Create virtual environment

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

### 3. Start Ollama

```bash
ollama serve
```

Make sure the model is available:

```bash
ollama pull llama3.2
```

### 4. Start FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Backend API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start Streamlit frontend

```bash
streamlit run frontend_app.py
```
---

## 🐳 Docker Setup

This project supports Docker-based local development with separate frontend and backend containers.

### Docker Architecture

```text
Browser
↓
Streamlit Frontend Container
↓ HTTP
FastAPI Backend Container
↓
Agent Router
↓
RAG Pipeline / AI Tools
↓
Chroma Vector Store
↓
Local Ollama Service
(host.docker.internal:11434)
```

### Run with Docker

Make sure Ollama is running locally:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Start the application using Docker Compose:

```bash
docker compose up
```

Frontend:

```text
http://localhost:8501
```

Backend API documentation:

```text
http://localhost:8000/docs
```

### Notes

The Docker backend communicates with the local Ollama service through:

```text
http://host.docker.internal:11434
```

This allows Docker containers to access the LLM service running on the host machine.

---

## 🎯 Key Highlights

- Designed and implemented a production-style RAG architecture
- Built a modular FastAPI backend and separated AI services from the frontend
- Implemented semantic retrieval using Chroma Vector Database and Sentence Transformers
- Improved answer quality using query rewriting and reranking techniques
- Developed a multi-tool AI Agent capable of selecting different tools based on user intent
- Implemented an extensible LLM provider factory supporting local and future cloud LLM services
- Containerized frontend and backend services using Docker and Docker Compose
- Designed the system with future cloud deployment and agent expansion in mind

---

## 📌 Future Improvements

- Replace rule-based routing with LLM-based Agent Router
- Integrate LangGraph for advanced multi-step tool calling
- Deploy the application to cloud platforms such as Render or Railway
- Add RAG evaluation metrics (retrieval accuracy, answer quality, latency)
- Migrate from Chroma to PostgreSQL + pgvector for production-level vector storage
- Build a React frontend for a more scalable user experience

---

## 👨‍💻 Author

**Zhipeng Lin**

AI Application Engineer | Data Analyst | Software Developer

GitHub:
https://github.com/zhipenglinpro-project

## 👨‍💻 Author

**Zhipeng L