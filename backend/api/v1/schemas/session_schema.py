from typing import List, Optional
from pydantic import BaseModel


class SessionMessage(BaseModel):
    role: str
    message: str


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[SessionMessage]
