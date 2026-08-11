import json
from crewai import Crew, Process, Task

from ai.agents.classifier_agent import classifier_agent
from ai.prompts.classifier_prompt import CLASSIFIER_TASK_DESCRIPTION
from core.logger import logger


def run_classifier(question: str) -> dict:
    task = Task(
        description=CLASSIFIER_TASK_DESCRIPTION.format(question=question),
        expected_output='{"category":"...","intent":"..."}',
        agent=classifier_agent,
    )

    crew = Crew(
        agents=[classifier_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    raw = result.raw.strip()

    try:
        parsed = json.loads(raw)
    except Exception:
        logger.exception("Classifier returned invalid JSON: %s", raw)
        parsed = {"category": "OutOfScope", "intent": "Unknown"}

    return parsed
