from crewai.flow import Flow, start

from ai.tasks.answer_task import run_answer_generator
from ai.tasks.qa_task import run_history_rewriter
from ai.tasks.question_task import run_classifier
from core.constants import ALLOWED_CATEGORIES, ALLOWED_INTENTS
from core.logger import logger
from models.search_question import RAGState
from repositories.search_repository import retrieve_documents
from repositories.session_repository import get_chat_history
from shared.helpers.context_builder import build_context
from shared.helpers.reranker import rerank_documents
from shared.utils.history_utils import history_query_rewrite
from shared.utils.intent_utils import intent_detection
from shared.utils.semantic_cache import (
    save_to_semantic_cache,
    semantic_cache_lookup,
)
from shared.validators.question_validator import validate_question


class HRRAGFlow(Flow[RAGState]):

    @start()
    def process_request(self):
        logger.info("=" * 80)
        logger.info("CrewAI HR RAG Flow Started")
        logger.info("Question: %s", self.state.question)

        # 1. Validation
        valid, message, normalized = validate_question(self.state.question)

        self.state.question = normalized
        self.state.is_valid = valid
        self.state.validation_message = message

        if not valid:
            self.state.answer = message
            return

        # 2. Rule-Based Intent Detection
        self.state.intent_route = intent_detection(self.state.question)
        self.state.detected_entities = {}

        if self.state.intent_route == "GREETING":
            self.state.answer = (
                "Hello! I'm your HR Assistant. " "How can I help you today?"
            )
            return

        if self.state.intent_route == "GOODBYE":
            self.state.answer = (
                "Thank you for contacting HR. " "Have a great day!"
            )
            return

        # 3. LLM Classification Crew
        try:
            result = run_classifier(self.state.question)

            category = result.get("category", "OutOfScope")
            intent = result.get("intent", "Unknown")

            if category not in ALLOWED_CATEGORIES:
                category = "OutOfScope"

            if intent not in ALLOWED_INTENTS:
                intent = "Unknown"

            self.state.query_category = category
            self.state.query_intent = intent

        except Exception:
            logger.exception("Classification failed")
            self.state.query_category = "OutOfScope"
            self.state.query_intent = "Unknown"

        # 4. History-Aware Query Rewriting
        self.state.history_question = self.state.question

        self.state.rewritten_question = history_query_rewrite(
            self.state.question,
            self.state.session_id,
            get_chat_history_func=get_chat_history,
            run_history_rewriter_func=run_history_rewriter,
        )

        # 5. Semantic Cache Lookup
        try:
            hit, cached_answer = semantic_cache_lookup(self.state)

            self.state.cache_hit = hit
            self.state.cache_answer = cached_answer

        except Exception:
            logger.exception("Semantic cache lookup failed")
            self.state.cache_hit = False
            self.state.cache_answer = ""

        if self.state.cache_hit:
            self.state.answer = self.state.cache_answer
            return

        # 6. Out Of Scope
        if self.state.query_category == "OutOfScope":
            self.state.answer = (
                "I'm an HR Policy Assistant. "
                "I can answer questions related to company HR policies, "
                "leave, attendance, payroll, insurance, travel, "
                "employee benefits, onboarding and other HR topics."
            )
            return

        # 7. Hybrid Retrieval
        self.state.retrieved_docs = retrieve_documents(self.state)

        # 8. Cross-Encoder Reranking
        self.state.reranked_docs = rerank_documents(
            query=self.state.rewritten_question,
            matches=self.state.retrieved_docs,
            top_k=5,
        )

        self.state.context, self.state.sources = build_context(
            self.state.reranked_docs
        )

        # 9. Final Answer Crew
        if not self.state.context.strip():
            self.state.answer = (
                "I couldn't find any matching HR policy documents."
            )
            return

        try:
            self.state.answer = run_answer_generator(self.state)
        except Exception:
            logger.exception("Answer generation failed")
            self.state.answer = (
                "I couldn't find that information in the HR policy documents."
            )

        # 10. Save Valid Answer To Semantic Cache
        invalid_answers = {
            "I couldn't find that information in the HR policy documents.",
            "I couldn't find any matching HR policy documents.",
        }

        if self.state.answer not in invalid_answers:
            save_to_semantic_cache(
                self.state,
                self.state.answer,
            )

        logger.info("CrewAI HR RAG Flow Completed")
        return self.state
