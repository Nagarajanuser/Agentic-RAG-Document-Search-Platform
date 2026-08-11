from crewai import Crew, Process, Task

from ai.agents.history_agent import history_agent
from ai.prompts.history_prompt import HISTORY_REWRITE_TASK_DESCRIPTION


def run_history_rewriter(history: str, question: str) -> str:
    task = Task(
        description=HISTORY_REWRITE_TASK_DESCRIPTION.format(
            history=history, question=question
        ),
        expected_output="One standalone HR question only.",
        agent=history_agent,
    )

    crew = Crew(
        agents=[history_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return result.raw.strip()
