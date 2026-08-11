from fastapi import APIRouter

from api.v1.schemas.evaluation_schema import (
    EvaluationRequest,
    EvaluationResponse,
)
from api.v1.services.evaluation_service import evaluate_response

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("/", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    return evaluate_response(request)
