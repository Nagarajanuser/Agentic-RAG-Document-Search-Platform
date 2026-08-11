from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ingest_no_file():
    response = client.post("/ingest")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["success"] is False
    assert json_resp["error"]["code"] == "INVALID_PAYLOAD"


@patch("api.v1.routes.ingest.save_and_ingest_uploaded_files")
def test_ingest_pdf_success(mock_save_and_ingest):
    mock_save_and_ingest.return_value = [
        {
            "filename": "test.pdf",
            "status": "success",
            "total_chunks": 3,
            "saved_path": "backend/pdfs/test.pdf"
        }
    ]

    fake_pdf_content = b"%PDF-1.4 test pdf content"
    files = {"file": ("test.pdf", fake_pdf_content, "application/pdf")}

    response = client.post("/ingest", files=files)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["success"] is True
    assert json_resp["data"]["processed_files"][0]["filename"] == "test.pdf"
    assert json_resp["data"]["processed_files"][0]["total_chunks"] == 3
