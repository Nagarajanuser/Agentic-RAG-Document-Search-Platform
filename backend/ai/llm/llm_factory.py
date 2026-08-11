from .ollama import llm as ollama_llm
from .openai import get_openai_llm


def get_llm(provider: str = "ollama"):
    if provider.lower() == "openai":
        return get_openai_llm()
    return ollama_llm
