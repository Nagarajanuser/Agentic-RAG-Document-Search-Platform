from crewai import Agent
from ai.llm.ollama import llm

history_agent = Agent(
    role="HR Conversation Query Rewriter",
    goal="Rewrite follow-up HR questions into standalone questions.",
    backstory=(
        "You understand conversational context and pronoun references. "
        "You preserve the exact meaning of the employee's question and never answer it."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
