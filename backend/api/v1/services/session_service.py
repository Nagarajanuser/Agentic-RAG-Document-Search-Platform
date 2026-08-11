from api.v1.schemas.session_schema import (
    SessionHistoryResponse,
    SessionMessage,
)
from repositories.session_repository import get_chat_history


def get_session_history(session_id: str) -> SessionHistoryResponse:
    history_str = get_chat_history(session_id, limit=20)
    messages = []
    for line in history_str.splitlines():
        if line.startswith("User: "):
            messages.append(SessionMessage(role="user", message=line[6:]))
        elif line.startswith("Assistant: "):
            messages.append(SessionMessage(role="assistant", message=line[11:]))
    return SessionHistoryResponse(session_id=session_id, messages=messages)
