import os
import sys

# Ensure stdout and stderr use UTF-8 in-place on Windows to handle unicode log characters/emojis cleanly
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

from core.logger import logger


def init_phoenix_tracing():
    """
    Initializes Phoenix OpenTelemetry tracing and LangChain/CrewAI instrumentation
    to visually inspect node executions, LLM calls, latency, inputs/outputs, and full RAG execution trace.
    """
    os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006"
    )

    try:
        from phoenix.otel import register
        from openinference.instrumentation.langchain import LangChainInstrumentor

        tracer_provider = register(
            project_name="hr-policy-rag",
        )

        LangChainInstrumentor().instrument(
            tracer_provider=tracer_provider
        )

        try:
            from openinference.instrumentation.crewai import CrewAIInstrumentor
            CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
            logger.info("CrewAI OpenInference instrumentation applied")
        except Exception as crew_err:
            logger.debug("CrewAI instrumentation skipped: %s", crew_err)

        logger.info("Phoenix tracing initialized")
        return tracer_provider

    except Exception as e:
        logger.warning("Phoenix tracing initialization skipped/failed: %s", e)
        return None
