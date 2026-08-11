from pinecone_text.hybrid import hybrid_convex_scale

from core.startup import bm25, embedding_model, index


def hybrid_search(
    query: str,
    top_k: int = 30,
    alpha: float = 0.7,
    metadata_filter: dict | None = None,
):
    if index is None or embedding_model is None or bm25 is None:
        return {"matches": []}

    dense = embedding_model.embed_query(query)
    sparse = bm25.encode_queries(query)

    dense, sparse = hybrid_convex_scale(
        dense,
        sparse,
        alpha=alpha,
    )

    return index.query(
        vector=dense,
        sparse_vector=sparse,
        top_k=top_k,
        include_metadata=True,
        filter=metadata_filter,
    )


def retrieve_documents(state):
    if not state.is_valid:
        return []

    if state.query_category == "OutOfScope":
        return []

    metadata_filter = {
        "$and": [
            {"department": {"$eq": state.department}},
            {"country": {"$eq": state.country}},
            {"access_level": {"$eq": state.access_level}},
            {"category": {"$eq": state.query_category}},
        ]
    }

    results = hybrid_search(
        state.rewritten_question,
        top_k=30,
        metadata_filter=metadata_filter,
    )

    raw_matches = (
        results.get("matches", [])
        if isinstance(results, dict)
        else getattr(results, "matches", [])
    )

    clean_matches = []
    for m in raw_matches:
        if isinstance(m, dict):
            clean_matches.append(m)
        elif hasattr(m, "to_dict"):
            clean_matches.append(m.to_dict())
        else:
            clean_matches.append(
                {
                    "id": getattr(m, "id", ""),
                    "score": float(getattr(m, "score", 0.0)),
                    "metadata": getattr(m, "metadata", {}) or {},
                }
            )

    return clean_matches

