from crewai import Task
from ai.agents.planner_agent import planner_agent
from ai.prompts.planner_prompt import PLANNER_TASK_DESCRIPTION


def build_planner_task() -> Task:
    return Task(
        description=PLANNER_TASK_DESCRIPTION,
        expected_output="An interview plan.",
        agent=planner_agent,
    )
