import asyncio
import json
import os
import sys
import types

# Fix for asyncio 'Event loop is closed' error on Windows during teardown
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Patch missing langchain_community chat model submodules required by Ragas
if "langchain_community.chat_models.vertexai" not in sys.modules:
    mod = types.ModuleType("langchain_community.chat_models.vertexai")
    mod.ChatVertexAI = type("ChatVertexAI", (), {})
    sys.modules["langchain_community.chat_models.vertexai"] = mod

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import components from production architecture
from ai.crews.interview_crew import HRRAGFlow
from core.security import logged_in_user
from core.startup import embedding_model
from datasets import Dataset
from langchain_ollama import ChatOllama
from models.interview_question import RAGState
from ragas import RunConfig, evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

ragas_llm = ChatOllama(model="qwen2.5:1.5b")


def ask_internal(question: str):
    """Runs one question through the HRRAGFlow pipeline."""
    flow = HRRAGFlow()
    flow.state.question = question
    flow.state.session_id = "eval_session"
    flow.state.department = logged_in_user["department"]
    flow.state.country = logged_in_user["country"]
    flow.state.location = logged_in_user["location"]
    flow.state.access_level = logged_in_user["access_level"]

    kickoff_result = flow.kickoff()

    if kickoff_result is None:
        result = flow.state
    elif isinstance(kickoff_result, RAGState):
        result = kickoff_result
    else:
        result = flow.state

    return {
        "answer": getattr(result, "answer", "") or "",
        "reranked_docs": getattr(result, "reranked_docs", []) or [],
    }


def load_questions():
    test_dataset_path = os.path.join(
        os.path.dirname(__file__), "test_dataset.json"
    )
    if not os.path.exists(test_dataset_path):
        test_dataset_path = "evaluation/test_dataset.json"

    with open(test_dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_evaluation_dataset():
    questions = load_questions()
    evaluation_dataset = []

    for item in questions:
        print("=" * 80)
        print("Question:", item["question"])

        result = ask_internal(item["question"])

        contexts = []
        for doc in result.get("reranked_docs", []):
            if isinstance(doc, dict) and "text" in doc:
                contexts.append(doc["text"])

        evaluation_dataset.append(
            {
                "user_input": item["question"],
                "retrieved_contexts": contexts,
                "response": result.get("answer", ""),
                "reference": item["ground_truth"],
            }
        )

        print("Answer:")
        print(result.get("answer", ""))

        print("\nRetrieved Contexts:")
        for i, context in enumerate(contexts, start=1):
            print(f"\nContext {i}")
            print(context)

    return evaluation_dataset


if __name__ == "__main__":
    dataset = build_evaluation_dataset()

    print("\n")
    print("=" * 80)
    print("Evaluation Dataset Built. Starting Ragas Evaluation...")
    print("=" * 80)

    hf_dataset = Dataset.from_list(dataset)

    try:
        result = evaluate(
            hf_dataset,
            metrics=[
                context_precision,
                context_recall,
                faithfulness,
                answer_relevancy,
            ],
            llm=ragas_llm,
            embeddings=embedding_model,
            raise_exceptions=False,
            # Set a high timeout because local LLMs can be slow
            run_config=RunConfig(timeout=300, max_workers=1),
        )

        print("\n" + "=" * 80)
        print("Ragas Evaluation Results")
        print("=" * 80)
        print(result)

        out_path = os.path.join(
            os.path.dirname(__file__), "ragas_results_latest.csv"
        )
        df = result.to_pandas()
        df.to_csv(out_path, index=False)
        print(f"\nResults saved to {out_path}")
    except Exception as e:
        print(f"\nRagas evaluation failed: {e}")