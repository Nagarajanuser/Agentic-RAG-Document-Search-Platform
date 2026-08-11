from fastapi import APIRouter

from api.v1.schemas.interview_schema import ApiResponse, QuestionRequest
from api.v1.services.interview_service import process_ask_request

router = APIRouter(tags=["Interview"])


@router.post("/ask", response_model=ApiResponse)
def ask_question(request: QuestionRequest):
    return process_ask_request(request)
