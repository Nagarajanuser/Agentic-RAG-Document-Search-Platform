from typing import Optional
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class Source(BaseModel):
    document: Optional[str] = None
    page: Optional[int] = None
    rerank_score: float
    pinecone_score: float


class QuestionResponse(BaseModel):
    question: str
    session_id: str
    answer: str
    sources: list[Source]


class ErrorResponse(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel):
    success: bool
    data: Optional[QuestionResponse]
    error: Optional[ErrorResponse]
