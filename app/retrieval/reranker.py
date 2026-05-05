def rerank_documents(question: str, docs, llm, top_k: int = 3):
    """
    用 LLM 对候选 chunks 重新打分，选出最相关的 top_k 个。
    返回：
    - top_docs
    - scored_docs  ([(score, doc), ...])
    """
    scored_docs = []

    for doc in docs:
        content = doc.page_content

        prompt = f"""
You are a relevance scoring assistant.

Score how useful the document is for answering the question.

Rules:
- Score from 0 to 10
- 10 = directly answers the question
- 7-9 = highly relevant
- 4-6 = somewhat relevant
- 0-3 = weak or irrelevant
- Output only the number

Question:
{question}

Document:
{content}

Score:
"""
        try:
            response = llm.invoke(prompt)
            score_text = response.content.strip()

            cleaned = "".join(ch for ch in score_text if ch.isdigit() or ch == ".")
            score = float(cleaned) if cleaned else 0.0
        except Exception:
            score = 0.0

        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = [doc for score, doc in scored_docs[:top_k]]

    return top_docs, scored_docs