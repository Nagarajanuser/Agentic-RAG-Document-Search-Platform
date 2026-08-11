from typing import Optional
from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    session_id: str
    question_id: Optional[str] = None
    user_answer: str


class EvaluationResponse(BaseModel):
    session_id: str
    score: float
    feedback: str
