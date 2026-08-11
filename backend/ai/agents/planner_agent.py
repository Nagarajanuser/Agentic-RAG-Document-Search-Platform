from crewai import Agent
from ai.llm.ollama import llm

planner_agent = Agent(
    role="Interview Planner",
    goal="Plan technical and domain-specific interview topics.",
    backstory="You structure structured multi-step technical interviews.",
    llm=llm,
    verbose=False,
    allow_delegation=False,
)
