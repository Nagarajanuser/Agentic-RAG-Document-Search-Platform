import re


def validate_question(question: str):
    question = question.strip()

    if not question:
        return False, "Please enter a question.", question

    if len(question) < 1:
        return False, "Please enter a more detailed question.", question

    if len(question) > 500:
        return False, "Question is too long.", question

    question = re.sub(r"\s+", " ", question)

    blocked_keywords = [
        "ignore previous instructions",
        "forget previous instructions",
        "system prompt",
        "show system prompt",
        "developer message",
        "reveal prompt",
        "bypass",
        "jailbreak",
        "act as",
        "pretend you are",
        "ignore all",
        "disable",
        "root access",
    ]

    lower_question = question.lower()

    for keyword in blocked_keywords:
        if keyword in lower_question:
            return (
                False,
                "Your question violates the HR Assistant usage policy.",
                question,
            )

    if "<script" in lower_question:
        return False, "Invalid question.", question

    sql_keywords = [
        "drop table",
        "delete from",
        "truncate",
        "insert into",
        "update ",
        "union select",
        "--",
    ]

    for keyword in sql_keywords:
        if keyword in lower_question:
            return False, "Invalid question.", question

    return True, "", question
