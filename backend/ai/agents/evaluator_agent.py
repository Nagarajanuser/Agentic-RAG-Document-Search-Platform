from crewai import Agent
from ai.llm.ollama import llm

evaluator_agent = Agent(
    role="Answer Evaluator",
    goal="Evaluate answers against rubric criteria.",
    backstory="You analyze responses for accuracy, clarity, and completeness.",
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
