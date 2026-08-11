HISTORY_REWRITE_TASK_DESCRIPTION = """
Rewrite the latest employee question into a standalone question.

Rules:
1. Use the conversation history.
2. Replace pronouns such as it, that, this, those, they and them.
3. Resolve references to earlier questions.
4. Preserve all meaning.
5. Never answer the question.
6. Return ONLY the rewritten question.
7. If the question is already self-contained, return it unchanged.

Conversation history:
{history}

Current question:
{question}
"""
