from crewai import LLM
from core.config import OLLAMA_BASE_URL

llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)
