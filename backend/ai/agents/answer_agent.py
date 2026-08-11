from crewai import Agent
from ai.llm.ollama import llm

answer_agent = Agent(
    role="Enterprise HR Policy Assistant",
    goal="Answer HR policy questions only from the supplied retrieved context.",
    backstory=(
        "You are a strict enterprise HR assistant. "
        "You do not use outside knowledge, do not guess, and do not fabricate."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
