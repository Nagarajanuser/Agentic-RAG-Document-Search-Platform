from typing import Optional
from pydantic import BaseModel


class EvaluationModel(BaseModel):
    evaluation_id: Optional[str] = None
    session_id: str
    score: float = 0.0
    feedback: Optional[str] = None
