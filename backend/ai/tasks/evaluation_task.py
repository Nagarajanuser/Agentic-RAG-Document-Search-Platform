from crewai import Task
from ai.agents.evaluator_agent import evaluator_agent
from ai.prompts.evaluation_prompt import EVALUATION_PROMPT


def build_evaluation_task() -> Task:
    return Task(
        description=EVALUATION_PROMPT,
        expected_output="An evaluation report with score and feedback.",
        agent=evaluator_agent,
    )
