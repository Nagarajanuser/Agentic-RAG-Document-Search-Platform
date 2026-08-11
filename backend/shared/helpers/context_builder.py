def build_context(reranked_docs):
    if not reranked_docs:
        return "", []

    context = ""
    sources = []

    for doc in reranked_docs:
        sources.append(
            {
                "document": doc["source"],
                "page": doc["page"],
                "rerank_score": doc["rerank_score"],
                "pinecone_score": doc["pinecone_score"],
            }
        )

        context += doc["text"] + "\n\n"

    return context, sources
