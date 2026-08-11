from core.constants import FOLLOWUP_PATTERNS
from core.logger import logger
from shared.utils.intent_utils import normalize_question


def is_followup_question(question: str) -> bool:
    question = normalize_question(question)
    words = question.split()

    for pattern in FOLLOWUP_PATTERNS:
        if " " in pattern:
            if pattern in question:
                return True
        elif pattern in words:
            return True

    return False


def history_query_rewrite(
    question: str, session_id: str, get_chat_history_func, run_history_rewriter_func
):
    if not is_followup_question(question):
        return question

    history = get_chat_history_func(session_id)

    if len(history.splitlines()) < 2:
        return question

    if not history.strip():
        return question

    try:
        rewritten = run_history_rewriter_func(history, question)
        return rewritten or question
    except Exception:
        logger.exception("History rewrite failed")
        return question
