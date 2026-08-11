from crewai import Agent
from ai.llm.ollama import llm

question_agent = Agent(
    role="Question Generator",
    goal="Generate targeted evaluation questions.",
    backstory="You construct interview questions based on specified guidelines.",
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
