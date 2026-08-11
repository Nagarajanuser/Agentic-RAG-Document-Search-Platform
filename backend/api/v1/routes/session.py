from fastapi import APIRouter

from api.v1.schemas.session_schema import SessionHistoryResponse
from api.v1.services.session_service import get_session_history

router = APIRouter(prefix="/session", tags=["Session"])


@router.get("/{session_id}", response_model=SessionHistoryResponse)
def get_history(session_id: str):
    return get_session_history(session_id)
