# 🤖 AI Multi-tool RAG Assistant

A modular, deployment-ready Retrieval-Augmented Generation (RAG) application built with FastAPI, LangChain, Ollama, Streamlit, and Docker.

The system supports document-based question answering, intelligent tool selection, and modular AI service architecture.

It enables users to upload documents and interact with a Multi-tool AI Agent that can answer questions, summarize documents, extract keywords, and provide knowledge base metadata.

---

## 📸 RAG Chatbot

![RAG Chatbot](screenshot.png)

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

## 🔄 Provider Switching Validation

The application supports both local and cloud-hosted Large Language Models through a provider abstraction layer implemented in `llm_factory.py`.

Provider selection is controlled through environment variables without requiring code changes.

Example:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

or

```env
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile
```

### Validation Results

| Provider | Status |
|-----------|----------|
| Ollama (Llama 3.2) | ✅ Tested |
| Groq (Llama 3.3 70B Versatile) | ✅ Tested |

Both providers were manually validated by switching environment variables and running the full application workflow without modifying application code.

---

## 🏗️ Engineering Decisions

### Why Chroma?

Chroma provides lightweight local vector storage with seamless LangChain integration, making it suitable for rapid development and experimentation.

Future production deployments could migrate to PostgreSQL + pgvector for improved scalability.

### Why Multiple LLM Providers?

Ollama enables fully local inference and offline experimentation.

Groq provides low-latency cloud-hosted inference.

A provider abstraction layer allows switching between local and cloud models without changing business logic.

### Why FastAPI?

FastAPI separates frontend and backend responsibilities, provides automatic OpenAPI documentation, and supports future deployment scenarios.

---

## 📂 Project Structure

```text
rag-chatbot/
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

## 📊 Evaluation

The RAG pipeline was manually evaluated across:

- Query rewriting
- Retrieval quality
- Reranking effectiveness
- Grounded answer generation
- Fallback handling
- Multi-tool routing

Summary:

- 9/9 evaluation scenarios passed
- 100% success rate

Detailed results:

See `EVALUATION.md`

---

## 🔄 CI/CD

This project includes automated validation through GitHub Actions.

The CI pipeline automatically runs:

- FastAPI endpoint tests
- Multi-tool routing tests
- Chat workflow tests

on every push and pull request.

Run locally:

```bash
pytest tests -v

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

## 🧪 Testing

The project includes automated tests covering API availability, multi-tool agent routing, and chat endpoint behaviour.

### Run All Tests

```bash
pytest tests -v
```

### Test Coverage

| Test File | Purpose |
|------------|----------|
| test_health.py | Validate FastAPI health endpoint |
| test_router.py | Validate multi-tool agent routing |
| test_chat.py | Validate chat API request/response flow |

### Example Result

```text
tests/test_health.py::test_health_endpoint PASSED

tests/test_router.py::test_route_to_summary PASSED
tests/test_router.py::test_route_to_keyword PASSED
tests/test_router.py::test_route_to_metadata PASSED
tests/test_router.py::test_route_to_rag PASSED

tests/test_chat.py::test_chat_endpoint_with_mock PASSED

========================
6 passed
========================
```

### Testing Strategy

- Health endpoint testing verifies API availability.
- Router tests validate tool selection logic.
- Chat endpoint tests validate request and response schemas.
- Mocked tests are used to isolate API behaviour from external LLM dependencies.

---


## ☁️ Deployment Note

This project is designed as a local-first AI application.

The complete RAG pipeline uses local vector storage, Sentence Transformers embeddings, and Ollama-based local LLM inference, which may exceed the memory limits of free cloud instances.

Therefore, the recommended demonstration environment is Docker-based local deployment.

The system also includes an extensible LLM provider abstraction layer, allowing future migration to cloud LLM services such as Groq or OpenAI without major architecture changes.

---

## 📌 Future Improvements

- Replace rule-based routing with LLM-based Agent Router
- Integrate LangGraph for advanced multi-step tool calling
- Optimize the architecture for lightweight cloud deployment on platforms such as Render or Railway
- Add RAG evaluation metrics (retrieval accuracy, answer quality, latency)
- Migrate from Chroma to PostgreSQL + pgvector for production-level vector storage
- Build a React frontend for a more scalable user experience

---

## 🚀 Roadmap

### Current Version

* FastAPI Backend
* Streamlit Frontend
* Chroma Vector Store
* Docker Compose Deployment
* Multi-tool Agent
* Ollama & Groq Provider Support

### Planned Improvements

* Automated Evaluation Framework
* Unit and API Testing
* LangGraph Agent Workflow
* PostgreSQL + pgvector
* Cloud-native Deployment
* React Frontend


---
## 👨‍💻 Author

**Zhipeng Lin**

AI Application Engineer | Data Analyst | Software Developer

GitHub:
https://github.com/zhipenglinpro-project/rag-chatbot

