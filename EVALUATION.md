# RAG Evaluation Report

This document contains representative test cases used to validate retrieval quality, query rewriting, reranking effectiveness, grounded answer generation, fallback behaviour, and multi-tool agent routing.

---

# Test Environment

### LLM
- Ollama (Llama 3.2)

### Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

### Vector Database
- Chroma

### Retrieval Configuration
- Initial Retrieval: Top 8 chunks
- Reranking: Top 3 chunks

---

# Query Rewrite Evaluation

## Test Case 1 — Pronoun Resolution

### Question 1
What is Chris learning?

### Question 2
What is his favorite food?

### Expected Rewrite
What is Chris's favorite food?

### Result
PASS

---

## Test Case 2 — Entity Resolution Failure Case

### Question 1
tell me about Amazon.

### Question 2
What does it do?

### Expected Rewrite
What does Amazon do?

### Actual Rewrite
What does Amazon do?

### Result
PASS

---

# Retrieval Evaluation

## Test Case 3 — Technology Retrieval

### Question
What technologies are used in this project?

### Expected Context
- Embeddings
- Vector Databases
- Retrieval-Augmented Generation (RAG)
- Local LLMs

### Relevant Context Retrieved
Yes

### Result
PASS

---

# Reranking Evaluation

## Test Case 4 — Retrieval Quality Optimisation

### Question
How is answer quality improved?

### Initial Retrieval
8 chunks

### After Reranking
3 chunks

### Relevant Chunks Prioritised
Yes

### Result
PASS

---

# Grounded Answer Evaluation

## Test Case 5 — Grounded Generation

### Question
What vector database does the project use?

### Answer
Chroma is a lightweight vector database often used in local RAG applications.

### Grounded In Retrieved Context
Yes

### Result
PASS

---

# Fallback Evaluation

## Test Case 6 — Out-of-Knowledge Question

### Question
Who won the FIFA World Cup in 2050?

### Expected Behaviour
No relevant information found in the knowledge base. Try rephrasing your question.

### Result
PASS

---

# Multi-tool Agent Evaluation

## Test Case 7 — Summary Tool

### Question
Summarize the document.

### Expected Tool
summary

### Expected Behaviour
Generate a concise document summary using uploaded knowledge base content.

### Result
PASS

---

## Test Case 8 — Keyword Extraction Tool

### Question
What are the key topics in the document?

### Expected Tool
keyword

### Expected Behaviour
Return the primary keywords or themes contained in the uploaded content.

### Result
PASS

---

## Test Case 9 — Metadata Tool

### Question
What tools are available?

### Expected Tool
metadata

### Expected Behaviour
Return available tool information and knowledge base metadata.

### Result
PASS

---

# Summary

| Category | Tests | Passed |
|-----------|--------|---------|
| Query Rewrite | 2 | 2 |
| Retrieval | 1 | 1 |
| Reranking | 1 | 1 |
| Grounded Answers | 1 | 1 |
| Fallback Behaviour | 1 | 1 |
| Multi-tool Agent | 3 | 3 |

### Overall Result

### Overall Result

9 / 9 Tests Passed

Success Rate: 100%

Note:
All representative test cases passed under the current evaluation setup. Additional edge-case testing is planned for query rewriting and entity resolution.

---

# Key Findings

### Strengths

- Query rewriting successfully handles basic pronoun resolution.
- Retrieval consistently returns relevant context from the vector store.
- Reranking reduces noise and improves answer grounding.
- Multi-tool agent routing works reliably across all implemented tools.
- Fallback behaviour prevents unsupported questions from producing hallucinated answers.

### Known Limitations

### Known Limitations

- Evaluation is currently based on manual testing and qualitative analysis.
- Query rewriting relies partially on entity extraction heuristics and may behave differently when named entities are not clearly identified (e.g. inconsistent capitalization).

### Future Improvements

- Add automated evaluation scripts.
- Expand test coverage with 20+ benchmark questions.
- Add latency and retrieval-quality metrics.
- Introduce automated unit and integration tests.