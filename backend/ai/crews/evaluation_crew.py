from crewai import Crew, Process
from ai.agents.evaluator_agent import evaluator_agent
from ai.tasks.evaluation_task import build_evaluation_task


def get_evaluation_crew() -> Crew:
    task = build_evaluation_task()
    return Crew(
        agents=[evaluator_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
