from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from api.v1.schemas.ingest_schema import (
    IngestApiResponse,
    IngestResponseData,
    IngestErrorResponse,
    IngestedFileSummary,
)
from api.v1.services.ingestion_service import save_and_ingest_uploaded_files
from core.logger import logger

router = APIRouter(tags=["Ingestion"])


@router.post("/ingest", response_model=IngestApiResponse)
async def ingest_documents(
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Endpoint to upload PDF documents as API payload to backend folder
    and run the ingestion pipeline. Accepts single file ('file') or multiple files ('files').
    """
    target_files: List[UploadFile] = []

    if files:
        target_files.extend(files)
    if file:
        target_files.append(file)

    if not target_files:
        return IngestApiResponse(
            success=False,
            data=None,
            error=IngestErrorResponse(
                code="INVALID_PAYLOAD",
                message="No PDF file payload provided. Please upload 'file' or 'files'.",
            ),
        )

    try:
        results = await save_and_ingest_uploaded_files(target_files)
        summaries = [IngestedFileSummary(**res) for res in results]

        return IngestApiResponse(
            success=True,
            data=IngestResponseData(
                message=f"Successfully processed {len(summaries)} PDF document(s).",
                processed_files=summaries,
            ),
            error=None,
        )
    except Exception as e:
        logger.exception("Error during PDF document ingestion")
        return IngestApiResponse(
            success=False,
            data=None,
            error=IngestErrorResponse(
                code="INGESTION_ERROR",
                message=str(e),
            ),
        )
