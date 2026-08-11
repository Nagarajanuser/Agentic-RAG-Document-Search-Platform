from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def home():
    return {"message": "HR Policy RAG API - CrewAI is running."}


@router.get("/health")
def health_check():
    return {"status": "ok"}
