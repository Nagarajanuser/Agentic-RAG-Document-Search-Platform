from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/status")
def admin_status():
    return {"status": "admin active"}
