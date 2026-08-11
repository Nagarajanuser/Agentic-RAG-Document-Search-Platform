from crewai import Crew, Process, Task

from ai.agents.answer_agent import answer_agent
from ai.prompts.answer_prompt import ANSWER_GENERATOR_TASK_DESCRIPTION


def run_answer_generator(state) -> str:
    task = Task(
        description=ANSWER_GENERATOR_TASK_DESCRIPTION.format(
            department=state.department,
            country=state.country,
            location=state.location,
            access_level=state.access_level,
            context=state.context,
            question=state.question,
        ),
        expected_output="A concise HR policy answer based only on the context.",
        agent=answer_agent,
    )

    crew = Crew(
        agents=[answer_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return result.raw.strip()
