import re
from core.constants import RULE_BASED_INTENTS


def normalize_question(question: str):
    question = question.lower()
    question = re.sub(r"[^a-z0-9 ]", " ", question)
    question = re.sub(r"\s+", " ", question)
    return question.strip()


def detect_rule_based(question: str):
    question = normalize_question(question)

    for intent, keywords in RULE_BASED_INTENTS.items():
        for keyword in keywords:
            if keyword in question:
                return intent

    return None


def intent_detection(question: str):
    intent = detect_rule_based(question)

    if intent is not None:
        return intent

    return "SEARCH_POLICY"
