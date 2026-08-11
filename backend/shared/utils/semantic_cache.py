import uuid
from datetime import datetime, timedelta, timezone

from core.constants import (
    CACHE_EXPIRY_DAYS,
    CACHE_THRESHOLD,
    CACHE_VERSION,
    EMBEDDING_MODEL_VERSION,
    MODEL_VERSION,
)
from core.logger import logger
from core.startup import cache_index, embedding_model


def save_to_semantic_cache(state, answer: str):
    try:
        if cache_index is None or embedding_model is None:
            logger.warning("Cache index or embedding model not initialized")
            return

        vector = embedding_model.embed_query(state.rewritten_question)
        doc_id = str(uuid.uuid4())

        metadata = {
            "question": state.question,
            "rewritten_question": state.rewritten_question,
            "answer": answer,
            "department": state.department,
            "country": state.country,
            "location": state.location,
            "access_level": state.access_level,
            "query_category": state.query_category,
            "query_intent": state.query_intent,
            "cache_version": CACHE_VERSION,
            "model_version": MODEL_VERSION,
            "embedding_model": EMBEDDING_MODEL_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        cache_index.upsert(
            vectors=[
                {
                    "id": doc_id,
                    "values": vector,
                    "metadata": metadata,
                }
            ]
        )

        logger.info("CACHE SAVED: %s", doc_id)

    except Exception:
        logger.exception("Semantic cache save failed")


def semantic_cache_lookup(state):
    if cache_index is None or embedding_model is None:
        return False, ""

    vector = embedding_model.embed_query(state.rewritten_question)

    metadata_filter = {
        "$and": [
            {"department": {"$eq": state.department}},
            {"country": {"$eq": state.country}},
            {"location": {"$eq": state.location}},
            {"access_level": {"$eq": state.access_level}},
            {"query_category": {"$eq": state.query_category}},
            {"cache_version": {"$eq": CACHE_VERSION}},
        ]
    }

    results = cache_index.query(
        vector=vector,
        top_k=1,
        include_metadata=True,
        filter=metadata_filter,
    )

    if not results.matches:
        return False, ""

    match = results.matches[0]
    similarity = match.score

    if similarity < CACHE_THRESHOLD:
        return False, ""

    created = datetime.fromisoformat(match.metadata["created_at"])
    age = datetime.now(timezone.utc) - created

    if age > timedelta(days=CACHE_EXPIRY_DAYS):
        return False, ""

    return True, match.metadata["answer"]
