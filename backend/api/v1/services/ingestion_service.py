import logging
import os
import re
import sys
import uuid
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from fastapi import UploadFile

try:
    from metadata import DOCUMENT_METADATA
except ImportError:
    DOCUMENT_METADATA = {}

# ---------------------------------------------------
# Setup Logger
# ---------------------------------------------------
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

# ---------------------------------------------------
# Helper functions for Pinecone & Embedding Lazy Initialization
# ---------------------------------------------------
_pinecone_index = None
_embedding_model = None


def get_pinecone_index():
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone
        key = os.getenv("PINECONE_API_KEY") or PINECONE_API_KEY
        idx_name = os.getenv("INDEX_NAME") or INDEX_NAME
        if not key:
            raise ValueError("PINECONE_API_KEY not found in .env")
        if not idx_name:
            raise ValueError("INDEX_NAME not found in .env")
        pc = Pinecone(api_key=key)
        _pinecone_index = pc.Index(idx_name)
    return _pinecone_index


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        _embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
    return _embedding_model


# ---------------------------------------------------
# Step 1 : Validate File
# ---------------------------------------------------
def validate_file(file_path: str):
    logger.info("validate_file : %s", file_path)
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    return path


# ---------------------------------------------------
# PDF Element Fallback Classes
# ---------------------------------------------------
class PDFElementMetadata:
    def __init__(self, page_number: int = 1):
        self.page_number = page_number


class NarrativeText:
    def __init__(self, text: str, page_number: int = 1):
        self.text = text
        self.metadata = PDFElementMetadata(page_number)


class Title:
    def __init__(self, text: str, page_number: int = 1):
        self.text = text
        self.metadata = PDFElementMetadata(page_number)


def _fallback_parse_pdf(file_path: str):
    logger.info("Using fallback PDF parser (pdfplumber) for: %s", file_path)
    import pdfplumber
    elements = []
    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            lines = text.splitlines()
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                # Determine if line looks like a title or narrative text
                if len(line_str.split()) <= 6 and (line_str[0].isdigit() or line_str.isupper()):
                    elements.append(Title(line_str, page_number=page_idx))
                else:
                    elements.append(NarrativeText(line_str, page_number=page_idx))
    return elements


# ---------------------------------------------------
# Step 2 : Parse PDF
# ---------------------------------------------------
def parse_pdf(file_path: str):
    logger.info("parse_pdf : %s", file_path)
    try:
        from unstructured.partition.pdf import partition_pdf
        elements = partition_pdf(
            filename=file_path,
            strategy="hi_res",
            infer_table_structure=True,
            languages=["eng"],
        )
        return elements
    except Exception as e:
        logger.warning("unstructured partition_pdf unavailable or failed (%s). Falling back to pdfplumber.", e)
        try:
            return _fallback_parse_pdf(file_path)
        except Exception as fallback_err:
            logger.error("Fallback PDF parsing failed: %s", fallback_err)
            raise RuntimeError(
                f"Failed to parse PDF document. Primary error: {e}. Fallback error: {fallback_err}"
            ) from e


# ---------------------------------------------------
# Step 3 : Clean Text
# ---------------------------------------------------
def clean_text(text: str) -> str:
    logger.info("clean_text : %s", text)
    if not text:
        return ""

    text = text.replace("\x00", "")
    text = re.sub(r"[-=_]{3,}", "", text)
    text = re.sub(r"Page\s+\d+(\s+of\s+\d+)?", "", text, flags=re.I)  # removed pdf's page number
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------
# Step 4 : Clean Elements
# ---------------------------------------------------
def clean_elements(elements):

    allowed = {
        "Title",
        "NarrativeText",
        "ListItem",
        "Table",
        "TableChunk",
        "CompositeElement",
        "Text",
    }

    cleaned = []

    for element in elements:

        if type(element).__name__ not in allowed:
            continue

        text = clean_text(element.text)

        if not text:
            continue

        element.text = text

        cleaned.append(element)
    return cleaned


# ---------------------------------------------------
# Step 4.1 : merge table rows
# ---------------------------------------------------
def merge_table_rows(elements):
    """
    Merge table-like key/value pairs that FAST parser splits.

    Example:

    Working Days
    Monday to Friday

    becomes

    Working Days : Monday to Friday
    """

    merged = []

    i = 0

    while i < len(elements):

        current = elements[i]

        current_text = clean_text(current.text)

        if i + 1 < len(elements):

            nxt = elements[i + 1]

            next_text = clean_text(nxt.text)

            current_type = type(current).__name__
            next_type = type(nxt).__name__

            # Table-like labels
            if (
                current_type == "Title"
                and next_type in ("NarrativeText", "Title")
                and len(current_text.split()) <= 4
                and not re.match(r'^\d+\.', current_text)
            ):

                current.text = f"{current_text}: {next_text}"

                merged.append(current)

                i += 2

                continue

        merged.append(current)

        i += 1

    return merged


# ---------------------------------------------------
# Step 5 : Chunk Elements (Section-aware Chunking)
# ---------------------------------------------------
def should_skip(text: str) -> bool:

    text = text.strip()

    # Remove only exact standalone header text
    if text == "Attendance Policy":
        return True

    if text == "New Gen Software Solutions":
        return True

    if re.fullmatch(r"Version:\s*[\d.]+", text):
        return True

    if re.fullmatch(r"Effective Date:.*", text):
        return True

    return False


SECTION_HEADING_PATTERN = re.compile(
    r"^\d+(\.\d+)*\.\s+[A-Z]"
)


def is_heading(element):

    text = element.text.strip()

    if not text:
        return False

    # Only numbered headings start a new chunk
    return bool(SECTION_HEADING_PATTERN.match(text))


def chunk_elements(elements):

    chunks = []

    current_title = None
    current_content = []
    current_page = None

    skip_section = False

    for element in elements:

        text = clean_text(element.text)

        if not text:
            continue

        if should_skip(text):
            continue

        # Ignore everything after Employee Acknowledgement
        if text.lower().startswith("employee acknowledgement") \
           or text.lower().startswith("employee acknowledgment"):

            skip_section = True
            continue

        if skip_section:
            continue

        if is_heading(element):

            if current_title:

                chunks.append({
                    "title": current_title,
                    "text": current_title + "\n\n" + "\n".join(current_content),
                    "page": current_page
                })

            current_title = text
            current_content = []
            current_page = getattr(
                element.metadata,
                "page_number",
                None
            )

        else:

            current_content.append(text)

    if current_title:

        chunks.append({
            "title": current_title,
            "text": current_title + "\n\n" + "\n".join(current_content),
            "page": current_page
        })

    logger.info("Total Chunks: %d", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        logger.info("=" * 80)
        logger.info("Chunk %d", i)
        logger.info("Title : %s", chunk['title'])
        logger.info("Page  : %s", chunk['page'])
        logger.info("Characters : %d", len(chunk['text']))
        logger.info("Words      : %d", len(chunk['text'].split()))
        logger.info("Text      : %s", chunk['text'])

    return chunks


# ---------------------------------------------------
# Step 6 : Attach Metadata
# ---------------------------------------------------
def build_documents(chunks, file_path):
    source = os.path.basename(file_path)
    base_metadata = DOCUMENT_METADATA.get(source, {})
    documents = []

    for chunk in chunks:
        logger.info('chunk %s', chunk)
        documents.append({
            "id": str(uuid.uuid4()),
            "text": chunk["text"],
            "metadata": {
                "source": source,
                "page": chunk["page"],
                "section": chunk["title"],
                **base_metadata
            }
        })

    return documents


# ---------------------------------------------------
# Step 7 : Create Embeddings
# ---------------------------------------------------
def create_embeddings(documents):
    """
    Generate embeddings for all document chunks in batch.
    Returns vectors ready for Pinecone upsert.
    """

    if not documents:
        return []

    # Collect all chunk texts
    texts = [doc["text"] for doc in documents]

    # Batch embedding (much faster than embed_query in a loop)
    embedding_model = get_embedding_model()
    embeddings = embedding_model.embed_documents(texts)

    vectors = []

    for doc, embedding in zip(documents, embeddings):
        metadata = doc["metadata"].copy()

        # Store chunk text for retrieval
        metadata["text"] = doc["text"]
        vectors.append(
            (
                doc["id"],          # Reuse existing UUID
                embedding,
                metadata
            )
        )

    return vectors


# ---------------------------------------------------
# Step 8 : Upload to Pinecone
# ---------------------------------------------------
def upload_to_pinecone(index, vectors, batch_size=100):
    total = len(vectors)
    for i in range(0, total, batch_size):
        batch = vectors[i:i + batch_size]
        try:
            index.upsert(vectors=batch)
            logger.info("Uploaded %d/%d", min(i + batch_size, total), total)

        except Exception as e:
            logger.error("Upload failed: %s", e)
            raise


# ---------------------------------------------------
# Complete Pipeline
# ---------------------------------------------------
def process_pdf(file_path):

    validate_file(file_path)

    elements = parse_pdf(file_path)

    elements1 = clean_elements(elements)

    elements2 = merge_table_rows(elements1)

    chunks = chunk_elements(elements2)

    documents = build_documents(chunks, file_path)

    vectors = create_embeddings(documents)

    index = get_pinecone_index()

    upload_to_pinecone(index, vectors)

    return documents


# ---------------------------------------------------
# Async/Payload handler for FastAPI endpoint
# ---------------------------------------------------
async def save_and_ingest_uploaded_files(upload_files: List[UploadFile], target_dir: str = "pdfs") -> List[dict]:
    """
    Saves uploaded PDF files to `target_dir` inside the backend directory
    and processes each file through the PDF ingestion pipeline.
    """
    base_backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dest_folder = os.path.join(base_backend_dir, target_dir)
    os.makedirs(dest_folder, exist_ok=True)

    results = []

    for upload_file in upload_files:
        filename = upload_file.filename or "uploaded.pdf"
        dest_path = os.path.join(dest_folder, filename)

        # Write uploaded contents to file
        content = await upload_file.read()
        with open(dest_path, "wb") as f:
            f.write(content)

        logger.info("Saved payload file to: %s", dest_path)

        # Process saved PDF
        documents = process_pdf(dest_path)

        results.append({
            "filename": filename,
            "status": "success",
            "total_chunks": len(documents),
            "saved_path": dest_path
        })

    return results
