from api.v1.schemas.interview_schema import (
    ApiResponse,
    ErrorResponse,
    QuestionResponse,
)


def create_success_response(question_response: QuestionResponse) -> ApiResponse:
    return ApiResponse(
        success=True,
        data=question_response,
        error=None,
    )


def create_error_response(
    message: str, code: str = "INTERNAL_SERVER_ERROR"
) -> ApiResponse:
    return ApiResponse(
        success=False,
        data=None,
        error=ErrorResponse(
            code=code,
            message=message,
        ),
    )
