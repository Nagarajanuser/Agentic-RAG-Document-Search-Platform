import os
from crewai import LLM


def get_openai_llm(model: str = "gpt-4o", temperature: float = 0.0):
    return LLM(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
    )
