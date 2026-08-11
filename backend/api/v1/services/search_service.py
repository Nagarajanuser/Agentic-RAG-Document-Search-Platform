import uuid

from ai.crews.search_crew import HRRAGFlow
from api.v1.schemas.search_schema import (
    ApiResponse,
    ErrorResponse,
    QuestionRequest,
    QuestionResponse,
)
from core.logger import logger
from core.security import logged_in_user
from models.search_question import RAGState
from repositories.session_repository import save_chat_message, save_chat_session


def process_ask_request(request: QuestionRequest) -> ApiResponse:
    logger.info("=" * 80)
    logger.info("New Request Received")
    logger.info("Question: %s", request.question)
    logger.info("Session: %s", request.session_id)

    if request.session_id is None:
        request.session_id = str(uuid.uuid4())

        save_chat_session(
            session_id=request.session_id,
            user_id=2,
        )

    save_chat_message(
        session_id=request.session_id,
        role="user",
        message=request.question,
    )

    try:
        flow = HRRAGFlow()

        flow.state.question = request.question
        flow.state.session_id = request.session_id

        flow.state.department = logged_in_user["department"]
        flow.state.country = logged_in_user["country"]
        flow.state.location = logged_in_user["location"]
        flow.state.access_level = logged_in_user["access_level"]

        kickoff_result = flow.kickoff()

        if kickoff_result is None:
            result = flow.state
        elif isinstance(kickoff_result, RAGState):
            result = kickoff_result
        else:
            result = flow.state

        if result is None:
            raise RuntimeError(
                "CrewAI Flow completed without producing RAG state."
            )

        answer = result.answer or ""

        save_chat_message(
            session_id=request.session_id,
            role="assistant",
            message=answer,
        )

        return ApiResponse(
            success=True,
            data=QuestionResponse(
                question=request.question,
                session_id=request.session_id,
                answer=answer,
                sources=result.sources or [],
            ),
            error=None,
        )

    except Exception as e:
        logger.exception("Error while processing /ask request")

        return ApiResponse(
            success=False,
            data=None,
            error=ErrorResponse(
                code="INTERNAL_SERVER_ERROR",
                message=str(e),
            ),
        )
