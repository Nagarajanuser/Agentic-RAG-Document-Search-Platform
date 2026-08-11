from typing import Optional
from pydantic import BaseModel


class InterviewSessionModel(BaseModel):
    session_id: str
    user_id: int
    created_at: Optional[str] = None
