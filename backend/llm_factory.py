import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv() ##load .env to os


def get_llm():
    """
    LLM factory.

    Current:
    - ollama for local development

    Future:
    - openai / groq / together for cloud deployment
    """

    provider = os.getenv("LLM_PROVIDER", "ollama")

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")