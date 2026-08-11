import os
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder
from sentence_transformers import CrossEncoder

from .config import INDEX_NAME, INDEX_NAME_CACHE, PINECONE_API_KEY
from .logger import logger

pc = None
index = None
cache_index = None
embedding_model = None
reranker = None
bm25 = None


def init_services():
    global pc, index, cache_index, embedding_model, reranker, bm25

    if PINECONE_API_KEY:
        try:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            if INDEX_NAME:
                index = pc.Index(INDEX_NAME)
            if INDEX_NAME_CACHE:
                cache_index = pc.Index(INDEX_NAME_CACHE)
        except Exception as e:
            logger.warning(f"Pinecone initialization failed: {e}")

    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            encode_kwargs={"normalize_embeddings": True},
        )
    except Exception as e:
        logger.warning(f"Embedding model initialization failed: {e}")

    try:
        reranker = CrossEncoder("BAAI/bge-reranker-base")
    except Exception as e:
        logger.warning(f"Reranker initialization failed: {e}")

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bm25_path = os.path.join(base_dir, "bm25_values.json")
        if not os.path.exists(bm25_path):
            bm25_path = "bm25_values.json"
        if os.path.exists(bm25_path):
            bm25 = BM25Encoder().load(bm25_path)
    except Exception as e:
        logger.warning(f"BM25 initialization failed: {e}")


# Initialize ML models & vector stores on module import
init_services()
