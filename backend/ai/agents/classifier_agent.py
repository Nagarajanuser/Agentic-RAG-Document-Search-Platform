from crewai import Agent
from ai.llm.ollama import llm

classifier_agent = Agent(
    role="Enterprise HR Query Classifier",
    goal="Classify employee HR questions into the allowed HR category and intent.",
    backstory=(
        "You are a strict enterprise HR query classifier. "
        "You never answer the question. You only classify it."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
