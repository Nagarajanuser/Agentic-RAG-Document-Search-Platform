from crewai import Agent
from ai.llm.ollama import llm

qa_agent = Agent(
    role="Quality Assurance Auditor",
    goal="Verify response quality and compliance.",
    backstory="You validate compliance against system prompts and policy safety.",
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
