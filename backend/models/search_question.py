from pydantic import BaseModel, Field


class RAGState(BaseModel):
    question: str = ""
    session_id: str = ""

    department: str = ""
    country: str = ""
    location: str = ""
    access_level: str = ""

    is_valid: bool = True
    validation_message: str = ""

    query_category: str = "OutOfScope"
    query_intent: str = "Unknown"

    intent_route: str = "SEARCH_POLICY"
    detected_entities: dict = Field(default_factory=dict)

    history_question: str = ""
    rewritten_question: str = ""

    cache_hit: bool = False
    cache_answer: str = ""

    retrieved_docs: list = Field(default_factory=list)
    reranked_docs: list = Field(default_factory=list)

    context: str = ""
    answer: str = ""

    sources: list = Field(default_factory=list)
