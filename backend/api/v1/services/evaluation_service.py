from api.v1.schemas.evaluation_schema import (
    EvaluationRequest,
    EvaluationResponse,
)


def evaluate_response(request: EvaluationRequest) -> EvaluationResponse:
    return EvaluationResponse(
        session_id=request.session_id,
        score=0.0,
        feedback="Evaluation complete.",
    )
